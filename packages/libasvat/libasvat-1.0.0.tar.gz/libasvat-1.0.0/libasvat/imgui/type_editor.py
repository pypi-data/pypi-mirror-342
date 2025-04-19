import types
import typing
import inspect
import libasvat.command_utils as cmd_utils
from enum import Enum
from imgui_bundle import imgui
from libasvat.imgui.math import Vector2
from libasvat.imgui.colors import Color, Colors
from libasvat.imgui.general import enum_drop_down, drop_down
from libasvat.utils import get_all_properties, AdvProperty, adv_property


class TypeDatabase(metaclass=cmd_utils.Singleton):
    """Database of Python Types and their TypeEditors for visualization and editing of values in IMGUI.

    NOTE: This is a singleton-class. All instances are the same, singleton instance.
    """

    def __init__(self):
        self._types: dict[type, type[TypeEditor]] = {}
        self._creatable_types: dict[type, bool] = {}

    def get_editor(self, value_type: type, config: dict[str, any] = None):
        """Creates a new TypeEditor instance for the given value type with the appropriate available TypeEditor class.

        This accepts regular ("actual") type objects and other type-hints, such as type aliases, generic types (``list[T]``)
        and union of types as the value_type.
        * For aliases/type-hints: the actual type (its origin) and sub-types (the hint's args) is used.
        * When handling actual type objects, its MRO is followed until we find a registered TypeEditor that handles that type.
        * For type unions, a specialized UnionEditor instance is returned.

        Args:
            value_type (type): The type to create the editor for.
            config (dict[str,any], optional): The configuration dict for the editor. These set the editor's attributes initial values.

        Returns:
            TypeEditor: A TypeEditor instance that can edit the given value_type, or None
            if no editor is registered for that type (or any of its parent classes).
        """
        actual_type = typing.get_origin(value_type) or value_type
        subtypes = typing.get_args(value_type)
        is_union = actual_type is types.UnionType
        editor_cls = None
        if is_union:
            editor_cls = UnionEditor
            actual_type = value_type  # UnionEditor needs original_type==value_type, being the union itself.
        else:
            for cls in actual_type.mro():
                if cls in self._types:
                    editor_cls = self._types[cls]
                    break
        if editor_cls:
            config = config or {}
            config["original_type"] = value_type
            config["value_type"] = actual_type
            config["value_subtypes"] = subtypes
            return editor_cls(config)

    def add_type_editor(self, cls: type, editor_class: type['TypeEditor'], is_creatable=True):
        """Adds a new TypeEditor class in this database associated with the given type.

        Args:
            cls (type): The value-type that the given Editor class can edit.
            editor_class (type[TypeEditor]): The TypeEditor class being added, that can edit the given ``cls`` type.
            is_creatable (bool, optional): If this type, with the given editor class, will be creatable via editor. Defaults to True.
        """
        self._types[cls] = editor_class
        self._creatable_types[cls] = is_creatable

    def get_creatable_types(self):
        """Gets the list of available types in the database that can be created simply with their editors.

        This is the list of all types that were registed as being creatable.

        Returns:
            list[type]: list of types with proper registered editors.
        """
        return [cls for cls, is_creatable in self._creatable_types.items() if is_creatable]

    @classmethod
    def register_editor_for_type(cls, type_cls: type, is_creatable=True):
        """[DECORATOR] Registers a decorated class as a TypeEditor for the given type-cls, in the TypeDatabase singleton.

        Thus, for example, this can be used as the following to register a string editor:
        ```python
        @TypeDatabase.register_editor_for_type(str)
        class StringEditor(TypeEditor):
            ...
        ```

        Args:
            type_cls (type): The value-type that the decorated Editor class can edit.
            is_creatable (bool, optional): If this type, with the given editor class, will be creatable via editor. Defaults to True.
        """
        def decorator(editor_cls):
            db = cls()
            db.add_type_editor(type_cls, editor_cls, is_creatable)
            return editor_cls
        return decorator

    @classmethod
    def register_noop_editor_for_this(cls, color: Color):
        """[DECORATOR] Registers a Noop Editor as TypeEditor for the decorated class.

        A NoopEditor is a editor that basically does nothing. It doesn't allow editing its value type.
        It's useful so that the editor system can still work for the type (the decorated class).

        NOTE: usage of this decorator is different from the ``register_editor_for_type``! Both are used to decorate classes,
        but this should be used on any class that you want to have a no-op type editor; while ``register_editor_for_type``
        is used to decorated a TypeEditor class, and register it as editor for a given type.

        Args:
            color (Color): Type color to set in the NoopEditor.
        """
        def decorator(type_cls):
            class SpecificNoopEditor(NoopEditor):
                def __init__(self, config: dict):
                    super().__init__(config)
                    self.color = color
            db = cls()
            db.add_type_editor(type_cls, SpecificNoopEditor, False)
            return type_cls
        return decorator


class ImguiProperty(AdvProperty):
    """IMGUI Property: an Advanced Property that associates a TypeEditor with the property.

    The TypeEditor can be used to render this property through IMGUI for editing. The editor's config
    is based on this property's metadata.
    """

    @property
    def editors(self) -> dict[object, 'TypeEditor']:
        """Internal mapping of objects to the TypeEditors that this property has created.
        The objects are the instances of the class that owns this property."""
        objects = getattr(self, "_editors", {})
        self._editors = objects
        return objects

    def get_value_from_obj(self, obj, owner: type | None = None):
        """Gets the internal value of this property in the given OBJ.

        This is similar to ``get_prop_value()``, but by default uses the property's getter, which may have been
        updated by subclasses."""
        return self.__get__(obj, owner)

    def get_prop_value(self, obj, owner: type | None = None):
        """Calls this property's getter on obj, to get its value.

        This is the property's common behavior (``return obj.property``).
        The Property subclasses (such as ImguiProperty or NodeDataProperty) may add logic to the getter, which is NOT called here.
        """
        return super().__get__(obj, owner)

    def set_prop_value(self, obj, value):
        """Calls this property's setter on obj to set the given value.

        This is essentially calling ``obj.property = value``, with one important difference: this calls the BASE setter!
        This does NOT call any extra logic that ImguiProperty subclasses may add to the setter method.
        """
        if self.fset:
            return super().__set__(obj, value)

    def restore_value(self, obj, value):
        """Calls this property's setter on obj to set the given value.

        This is meant to emulate the regular "set attribute" logic (``obj.property = value``).

        While ``self.set_prop_value()`` calls the base setter specifically (and most likely should remain that way), this
        method may be overwritten by subclasses to perform their proper logic when setting a value without the caller explicitly
        using ``self.__set__()``. The default implementation in ImguiProperty uses ``set_prop_value()``.
        """
        return self.set_prop_value(obj, value)

    def get_value_type(self, obj=None):
        """Gets the type of this property (the type of its value).

        This checks the return type-hint of the property's getter method.
        If no return type is defined, and ``obj`` is given, this tries getting the type
        from the actual value returned by this property.

        Args:
            obj (optional): The object that owns this property. Defaults to None (getting the type based on type-hint).

        Returns:
            type: the type of this property. In failure cases, this might be:
            * ``inspect._empty``, if the property's getter has no return type annotation, and given ``obj`` was None.
            * The actual type of the value returned by the property, if the getter has no return type annotation and given ``obj`` as valid.
            This "actual type" might not be the desired/expected type of the property. For example, could be a class of some kind but value was None.
        """
        sig = inspect.signature(self.fget)
        cls = sig.return_annotation
        if cls == sig.empty:
            if "value_type" in self.metadata:
                return self.metadata["value_type"]
            elif obj is not None:
                # Try getting type from property getter return value.
                return type(self.fget(obj))
        return cls

    def get_value_subtypes(self) -> tuple[type, ...]:
        """Gets the subtypes of this property (the subtypes of its value-type).

        Types that act as containers of objects (such as lists, dicts and so on) can define the types they contain - these are the subtypes.
        Consider the following examples for the property's type:
        * ``list[str]``: the ``list`` type is the property's base type, the one returned by ``self.get_value_type()``. But ``str`` is its subtype,
        the expected type of objects the list will contain.
        * Same goes for ``dict[int, float]``: dict is the base type, ``(int, float)`` will be the subtypes.

        Returns:
            tuple[type, ...]: a tuple of subtypes. This tuple will be empty if there are no subtypes.
        """
        sig = inspect.signature(self.fget)
        cls = sig.return_annotation
        if cls == sig.empty:
            return tuple()
        return typing.get_args(cls)

    def get_editor_config(self):
        """Gets the TypeEditor config dict used to initialize editors for this property, for
        the given object (property owner).

        Returns:
            dict: the config dict to pass to a TypeEditor's constructor.
        """
        config = self.metadata.copy()
        if "doc" not in config:
            config["doc"] = self.__doc__ or ""
        return config

    def get_editor(self, obj):
        """Gets the TypeEditor instance for the given object, for editing this property's value.

        This property stores a table of obj->TypeEditor instances. So each object will always use the same
        editor for its property. If the editor instance doesn't exist, one will be created according to our value-type,
        passing this property's metadata as config.

        Args:
            obj (any): The object that owns this property. A property is created as part of a class, thus this object
            is a instance of that class.

        Returns:
            TypeEditor: The TypeEditor instance for editing this property, in this object. None if the editor instance doesn't
            exist and couldn't be created (which usually means the property's value type is undefined, or no Editor class is
            registered for it).
        """
        editor: TypeEditor = self.editors.get(obj, None)
        if editor is None:
            database = TypeDatabase()
            config = self.get_editor_config()
            editor = database.get_editor(self.get_value_type(obj), config)
            self.editors[obj] = editor
        return editor

    def render_editor(self, obj):
        """Renders the TypeEditor for editing this property through IMGUI.

        This gets the TypeEditor for this property and object from ``self.get_editor(obj)``, and calls its ``render_property`` method
        to render the editor.
        If the editor is None, display a error message in imgui instead.

        Args:
            obj (any): The object that owns this property.

        Returns:
            bool: If the property's value was changed.
        """
        editor = self.get_editor(obj)
        if editor:
            return editor.render_property(obj, self.name)
        # Failsafe if no editor for our type exists
        imgui.text_colored(Colors.red, f"{type(obj).__name__} property '{self.name}': No TypeEditor exists for type '{self.get_value_type(obj)}'")
        return False


def imgui_property(**kwargs):
    """Imgui Property attribute. Can be used to create imgui properties the same way as a regular @property.

    A imgui-property behaves exactly the same way as a regular python @property, but also includes associated
    metadata used to build a TypeEditor for that property's value type for each object that uses that property.
    With this, the property's value can be easily seen or edited in IMGUI.

    There are also related ``<type>_property`` decorators defined here, as an utility to setup the property metadata
    for a specific type.
    """
    return adv_property(kwargs, ImguiProperty)


# Other colors:
#   object/table: blue
#   array: yellow   ==>used on Enum
#   generic: (0.2, 0.2, 0.6, 1)  ==>used as default color in TypeEditor
######################
# TODO: Possivelmente mover classes de editores pra vários outros módulos.
# TODO: refatorar esse sistema pra não ser tão rigido. Usando reflection pra ler as type_hints da property
#   pra pegar os editors certos automaticamente. Isso facilitaria muito o uso.
#   - Ter uma classe com propriedades bem tipadas seria suficiente pra gerar os editors dela. Não precisaria hardcodar imgui_properties e tal
#     mas ainda poderia ter uma "property" diferente que guarda um **kwargs de metadata de tal property, que seria usado como a config do
#     modelo de tal atributo
# TODO: refatorar pra permitir cascata facilmente (lista com listas com listas... ou dicts com dicts e por ai vai)
#   assim a funcionalidade ficaria mais próxima do TPLove TableEditor, permitindo estruturas de dados quaisquer.
# TODO: refatorar pra ser fácil poder ter valor None sem quebrar as coisas.
#   - talvez uma flag "can be None?" ou algo assim nos editors?
class TypeEditor:
    """Basic class for a value editor in imgui.

    This allows rendering controls for editing a specific type in IMGUI, and also allows rendering
    properties/attributes of that type using a ``key: value`` display, allowing the user to edit the value.

    Subclasses of this represent an editor for a specific type, and thus implement the specific imgui control
    logic for that type by overriding just the ``draw_value_editor`` method.

    The ``TypeDatabase`` singleton can be used to get the TypeEditor class for a given type, and to register
    new editors for other types.

    The ``@imgui_property(metadata)`` decorator can be used instead of ``@property`` to mark a class' property as being an
    "Imgui Property". They have an associated TypeEditor based on the property's type, with metadata for the editor
    passed in the decorator. When rendering, a object of the class may update its editor by having specific methods
    (see ``update_from_obj``). The ``render_all_properties()`` function can then be used to render all available
    ImguiProperties in a object.

    Other ``@<type>_property(**args)`` decorators exist to help setting up a imgui-property by having documentation for
    the metadata of that type.
    """

    def __init__(self, config: dict):
        self.original_type: type = config.get("original_type")
        """The original type used to create this Editor instance. This might be any kind of type-hint, such as
        an actual type object, a union of types, type aliases, and so on. See ``self.value_type`` and ``self.value_subtypes``."""
        self.value_type: type = config.get("value_type")
        """The actual type object of our expected value."""
        self.value_subtypes: tuple[type, ...] = config.get("value_subtypes")
        """The subtypes (or "arg" types) of our value-type. This is always a tuple of types, and might be empty if no subtypes exist.
        This is used when the original-type is a type-hint that "contains" or "uses" other types, such as:
        * For example, if original is ``list[T]``, subtypes will be ``(T,)`` while the value-type is ``list``.
        * Another example, if original is ``dict[K,V]``, subtypes will be ``(K,V)`` while value-type is ``dict``.
        * For a union type, the subtypes is a tuple of all types in the union.
        """
        self.attr_doc = config.get("doc", "")
        """The value's docstring, usually used as a tooltip when editing to explain that value.

        When TypeEditor is created from a imgui-property, by default this value is the property's docstring.
        """
        self.add_tooltip_after_value = True
        """If true, this will add ``self.attr_doc`` as a tooltip for the last imgui control drawn."""
        self.color: Color = Color(0.2, 0.2, 0.6, 1)
        """Color of this type. Mostly used by DataPins of this type in Node Systems."""
        self.extra_accepted_input_types: type | tuple[type] | types.UnionType = None
        """Extra types that this editor, when used as a Input DataPin in Node Systems, can accept as value.
        Useful for types that can accept (or convert) other values to its type.

        These extra types can be defined the same way as the ``class_or_tuple`` param for ``issubclass(type, class_or_tuple)``.
        Which means, it can be a single type, a UnionType (``A | B``) or a tuple of types.

        This is usually used together with ``self.convert_value_to_type`` to ensure the input value is converted
        to this type.
        """
        self.convert_value_to_type = False
        """If the value we receive should be converted to our ``value_type`` before using. This is done using
        ``self.value_type(value)``, like most basic python types accept."""

    def type_name(self):
        """Gets a human readable name of the type represented by this editor."""
        return self.value_type.__name__

    def render_property(self, obj, name: str):
        """Renders this type editor as a KEY:VALUE editor for a ``obj.name`` property/attribute.

        This also allows the object to automatically update this editor before rendering the key:value controls.
        See ``self.update_from_obj`` (which is called from here).

        Args:
            obj (any): the object being updated
            name (str): the name of the attribute in object we're editing.

        Returns:
            bool: if the property's value was changed.
            If so, the new value was set in the object automatically.
        """
        self.update_from_obj(obj, name)
        imgui.text(f"{name}:")
        imgui.set_item_tooltip(self.attr_doc)
        imgui.same_line()

        value = getattr(obj, name)
        value = self._check_value_type(value)
        changed, new_value = self.render_value_editor(value)
        if changed:
            setattr(obj, name, new_value)
        return changed

    def render_value_editor[T](self, value: T) -> tuple[bool, T]:
        """Renders the controls for editing a value of type T, which should be the type expected by this TypeEditor instance.

        This pushes/pops an ID from imgui's ID stack, calls ``self.draw_value_editor`` and optionally sets an item tooltip
        for the last imgui control drawn by ``draw_value_editor`` (see ``self.add_tooltip_after_value``).

        So this method wraps ``draw_value_editor`` with a few basic operations. Subclasses should NOT overwrite this, overwrite
        ``draw_value_editor`` instead to implement their logic. This method is the one that should be used to render the type controls
        to edit a value.

        Args:
            value (T): the value to change.

        Returns:
            tuple[bool, T]: returns a ``(changed, new_value)`` tuple.
        """
        imgui.push_id(f"{repr(self)}")
        value = self._check_value_type(value)
        changed, new_value = self.draw_value_editor(value)
        if self.add_tooltip_after_value:
            imgui.set_item_tooltip(self.attr_doc)
        imgui.pop_id()
        return changed, new_value

    def draw_value_editor[T](self, value: T) -> tuple[bool, T]:
        """Draws the controls for editing a value of type T, which should be the type expected by this TypeEditor instance.

        This is type-specific, and thus should be overriden by subclasses to implement their logic.

        Args:
            value (T): the value to change.

        Returns:
            tuple[bool, T]: returns a ``(changed, new_value)`` tuple.
        """
        raise NotImplementedError

    def update_from_obj(self, obj, name: str):
        """Calls a optional ``<OBJ>._update_<NAME>_editor(self)`` method from the given object,
        with the purpose of dynamically updating this editor's attributes before drawing the editor itself.

        Args:
            obj (any): the object being updated
            name (str): the name of the attribute in object we're editing.
        """
        updater_method_name = f"_update_{name}_editor"
        method = getattr(obj, updater_method_name, None)
        if method is not None:
            method(self)

    def _check_value_type[T](self, value: T) -> T:
        """Checks and possibly converts the given value to our value-type if required.

        Args:
            value (T): the value to type-check.

        Returns:
            T: the value, converted to our ``self.value_type`` if required and possible.
            If conversion is not required, returns the same value received.
            If conversion is required but fails with a TypeError and value is None, will return ``self.value_type()`` to create a default
            value of our type, otherwise will (re)raise the error from the conversion.
        """
        if self.convert_value_to_type and self.value_type and not isinstance(value, self.value_type):
            try:
                value = self.value_type(value)
            except TypeError:
                if value is None:
                    # Common type conversion can fail if value=None. So just try to generate a default value.
                    # Most basic types in python (int, float, str, bool...) follow this behavior.
                    value = self.value_type()
                else:
                    # If conversion failed and type wasn't None, then we have a real error on our hands. Re-raise the exception to see it.
                    raise
        return value


@TypeDatabase.register_editor_for_type(str)
class StringEditor(TypeEditor):
    """Imgui TypeEditor for editing a STRING value."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.flags: imgui.InputTextFlags_ = config.get("flags", imgui.InputTextFlags_.none)
        # String Enums attributes
        self.options: list[str] = config.get("options")
        self.docs: list[str] | dict[str, str] | None = config.get("docs")
        self.option_flags: imgui.SelectableFlags_ = config.get("option_flags", 0)
        self.add_tooltip_after_value = self.options is None
        self.multiline: bool = config.get("multiline", False)
        self.color = Colors.magenta
        self.extra_accepted_input_types = object
        self.convert_value_to_type = True

    def draw_value_editor(self, value: str) -> tuple[bool, str]:
        if self.options is None:
            if value is None:
                value = ""
            num_lines = value.count("\n") + 1
            if self.multiline or num_lines > 1:
                size = (0, num_lines * imgui.get_text_line_height_with_spacing())
                changed, new_value = imgui.input_text_multiline("##", value, size, flags=self.flags)
            else:
                changed, new_value = imgui.input_text("##", value, flags=self.flags)
            return changed, new_value.replace("\\n", "\n")
        else:
            return drop_down(value, self.options, self.docs, default_doc=self.attr_doc, item_flags=self.option_flags)


def string_property(flags: imgui.InputTextFlags_ = 0, options: list[str] = None, docs: list | dict = None, option_flags: imgui.SelectableFlags_ = 0):
    """Imgui Property attribute for a STRING type.

    Behaves the same way as a property, but includes a StringEditor object for allowing changing this string's value in imgui.

    Args:
        flags (imgui.InputTextFlags_, optional): flags to pass along to ``imgui.input_text``. Defaults to None.
        options (list[str]): List of possible values for this string property. If given, the editor control changes to a drop-down
        allowing the user to select only these possible values.
        docs (list | dict, optional): Optional definition of documentation for each option, shown as a tooltip (for that option) in the editor.
        Should be a ``list[str]`` matching the length of ``options``, or a ``{option: doc}`` dict. The property's docstring is used as a default
        tooltip for all options.
        option_flags (imgui.SelectableFlags_, optional): Flags passed down to the drop-down selectable.
    """
    return imgui_property(flags=flags, options=options, docs=docs, option_flags=option_flags)


@TypeDatabase.register_editor_for_type(Enum, False)
class EnumEditor(TypeEditor):
    """Imgui TypeEditor for editing a ENUM value."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.add_tooltip_after_value = False
        self.color = Colors.yellow
        self.flags: imgui.SelectableFlags_ = config.get("flags", 0)

    def draw_value_editor(self, value: str | Enum) -> tuple[bool, str | Enum]:
        return enum_drop_down(value, self.attr_doc, self.flags)


def enum_property(flags: imgui.SelectableFlags_ = 0):
    """Imgui Property attribute for a ENUM type.

    Behaves the same way as a property, but includes a EnumEditor object for allowing changing this enum's value in imgui.

    Args:
        flags (imgui.SelectableFlags_, optional): Flags passed down to the drop-down selectable.
    """
    return imgui_property(flags=flags)


@TypeDatabase.register_editor_for_type(bool)
class BoolEditor(TypeEditor):
    """Imgui TypeEditor for editing a BOOLEAN value."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.color = Colors.red
        self.extra_accepted_input_types = object
        self.convert_value_to_type = True

    def draw_value_editor(self, value: bool):
        return imgui.checkbox("##", value)


def bool_property():
    """Imgui Property attribute for a BOOL type.

    Behaves the same way as a property, but includes a BoolEditor object for allowing changing this bool's value in imgui.
    """
    return imgui_property()


@TypeDatabase.register_editor_for_type(float)
class FloatEditor(TypeEditor):
    """Imgui TypeEditor for editing a FLOAT value."""

    def __init__(self, config: dict):
        """
        Args:
            min (float, optional): Minimum allowed value for this float property. Defaults to 0.0.
            max (float, optional): Maximum allowed value for this float property. Defaults to 0.0. If MIN >= MAX then we have no bounds.
            format (str, optional): Text format of the value to decorate the control with. Defaults to "%.2f". Apparently this needs to be a valid
            python format, otherwise the float control wont work properly.
            speed (float, optional): Speed to apply when changing values. Only applies when dragging the value and IS_SLIDER=False. Defaults to 1.0.
            is_slider (bool, optional): If we'll use a SLIDER control for editing. It contains a marker indicating the value along the range between
            MIN<MAX (if those are valid). Otherwise defaults to using a ``drag_float`` control. Defaults to False.
            flags (imgui.SliderFlags_, optional): Flags for the Slider/Drag float controls. Defaults to imgui.SliderFlags_.none.
        """
        super().__init__(config)
        self.is_slider: bool = config.get("is_slider", False)
        """If the float control will be a slider to easily choose between the min/max values. Otherwise the float control will
        be a drag-float."""
        self.speed: float = config.get("speed", 1.0)
        """Speed of value change when dragging the control's value. Only applies when using drag-controls (is_slider=False)"""
        self.min: float = config.get("min", 0.0)
        """Minimum value allowed. For proper automatic bounds in the control, ``max`` should also be defined, and be bigger than this minimum.
        Also use the ``always_clamp`` slider flags."""
        self.max: float = config.get("max", 0.0)
        """Maximum value allowed. For proper automatic bounds in the control, ``min`` should also be defined, and be lesser than this maximum.
        Also use the ``always_clamp`` slider flags."""
        self.format: str = config.get("format", "%.2f")
        """Format to use to convert value to display as text in the control (use python float format, such as ``%.2f``)"""
        self.flags: imgui.SliderFlags_ = config.get("flags", 0)
        """Slider flags to use in imgui's float control."""
        self.color = Colors.green
        self.convert_value_to_type = True
        self.extra_accepted_input_types = int

    def draw_value_editor(self, value: float):
        if value is None:
            value = 0.0
        if self.is_slider:
            return imgui.slider_float("##value", value, self.min, self.max, self.format, self.flags)
        else:
            return imgui.drag_float("##value", value, self.speed, self.min, self.max, self.format, self.flags)


def float_property(min=0.0, max=0.0, format="%.2f", speed=1.0, is_slider=False, flags: imgui.SliderFlags_ = 0):
    """Imgui Property attribute for a FLOAT type.

    Behaves the same way as a property, but includes a FloatEditor object for allowing changing this float's value in imgui.

    Args:
        min (float, optional): Minimum allowed value for this float property. Defaults to 0.0.
        max (float, optional): Maximum allowed value for this float property. Defaults to 0.0. If MIN >= MAX then we have no bounds.
        format (str, optional): Text format of the value to decorate the control with. Defaults to "%.3". Apparently this needs to be a valid
        python format, otherwise the float control wont work properly.
        speed (float, optional): Speed to apply when changing values. Only applies when dragging the value and IS_SLIDER=False. Defaults to 1.0.
        is_slider (bool, optional): If we'll use a SLIDER control for editing. It contains a marker indicating the value along the range between
        MIN<MAX (if those are valid). Otherwise defaults to using a ``drag_float`` control. Defaults to False.
        flags (imgui.SliderFlags_, optional): Flags for the Slider/Drag float controls. Defaults to imgui.SliderFlags_.none.
    """
    return imgui_property(min=min, max=max, format=format, speed=speed, is_slider=is_slider, flags=flags)


@TypeDatabase.register_editor_for_type(int)
class IntEditor(TypeEditor):
    """Imgui TypeEditor for editing a INTEGER value."""

    def __init__(self, config: dict):
        """
        Args:
            min (int, optional): Minimum allowed value for this int property. Defaults to 0.
            max (int, optional): Maximum allowed value for this int property. Defaults to 0. If MIN >= MAX then we have no bounds.
            format (str, optional): Text format of the value to decorate the control with. Defaults to "%d". Apparently this needs to be a valid
            python format, otherwise the int control wont work properly.
            speed (float, optional): Speed to apply when changing values. Only applies when dragging the value and IS_SLIDER=False. Defaults to 1.0.
            is_slider (bool, optional): If we'll use a SLIDER control for editing. It contains a marker indicating the value along the range between
            MIN<MAX (if those are valid). Otherwise defaults to using a ``drag_int`` control. Defaults to False.
            flags (imgui.SliderFlags_, optional): Flags for the Slider/Drag int controls. Defaults to imgui.SliderFlags_.none.
        """
        super().__init__(config)
        self.is_slider: bool = config.get("is_slider", False)
        """If the int control will be a slider to easily choose between the min/max values. Otherwise the int control will
        be a drag-int."""
        self.speed: float = config.get("speed", 1.0)
        """Speed of value change when dragging the control's value. Only applies when using drag-controls (is_slider=False)"""
        self.min: int = config.get("min", 0)
        """Minimum value allowed. For proper automatic bounds in the control, ``max`` should also be defined, and be bigger than this minimum.
        Also use the ``always_clamp`` slider flags."""
        self.max: int = config.get("max", 0)
        """Maximum value allowed. For proper automatic bounds in the control, ``min`` should also be defined, and be lesser than this maximum.
        Also use the ``always_clamp`` slider flags."""
        self.format: str = config.get("format", "%d")
        """Format to use to convert value to display as text in the control (use python int format, such as ``%d``)"""
        self.flags: imgui.SliderFlags_ = config.get("flags", 0)
        """Slider flags to use in imgui's int control."""
        self.color = Colors.cyan
        self.convert_value_to_type = True
        self.extra_accepted_input_types = float

    def draw_value_editor(self, value: int):
        if value is None:
            value = 0
        if self.is_slider:
            return imgui.slider_int("##value", value, self.min, self.max, self.format, self.flags)
        else:
            return imgui.drag_int("##value", value, self.speed, self.min, self.max, self.format, self.flags)


def int_property(min=0, max=0, format="%d", speed=1, is_slider=False, flags: imgui.SliderFlags_ = 0):
    """Imgui Property attribute for a INTEGER type.

    Behaves the same way as a property, but includes a IntEditor object for allowing changing this int's value in imgui.

    Args:
        min (int, optional): Minimum allowed value for this int property. Defaults to 0.
        max (int, optional): Maximum allowed value for this int property. Defaults to 0. If MIN >= MAX then we have no bounds.
        format (str, optional): Text format of the value to decorate the control with. Defaults to "%d". Apparently this needs to be a valid
        python format, otherwise the int control wont work properly.
        speed (float, optional): Speed to apply when changing values. Only applies when dragging the value and IS_SLIDER=False. Defaults to 1.
        is_slider (bool, optional): If we'll use a SLIDER control for editing. It contains a marker indicating the value along the range between
        MIN<MAX (if those are valid). Otherwise defaults to using a ``drag_int`` control. Defaults to False.
        flags (imgui.SliderFlags_, optional): Flags for the Slider/Drag int controls. Defaults to imgui.SliderFlags_.none.
    """
    return imgui_property(min=min, max=max, format=format, speed=speed, is_slider=is_slider, flags=flags)


@TypeDatabase.register_editor_for_type(Color)
class ColorEditor(TypeEditor):
    """Imgui TypeEditor for editing a COLOR value."""

    def __init__(self, config: dict):
        # flags: imgui.ColorEditFlags_ = imgui.ColorEditFlags_.none
        super().__init__(config)
        self.flags: imgui.ColorEditFlags_ = config.get("flags", 0)
        self.color = Color(1, 0.5, 0.3, 1)
        self.convert_value_to_type = True

    def draw_value_editor(self, value: Color):
        if value is None:
            value = imgui.ImVec4(1, 1, 1, 1)
        changed, new_value = imgui.color_edit4("##", value, self.flags)
        if changed:
            value = Color(*new_value)
        return changed, value


def color_property(flags: imgui.ColorEditFlags_ = imgui.ColorEditFlags_.none):
    """Imgui Property attribute for a COLOR type.

    Behaves the same way as a property, but includes a ColorEditor object for allowing changing this color's value in imgui.
    """
    return imgui_property(flags=flags)


# TODO: isso ta QUEBRADO! Mas não tá sendo usado, então pode ser totalmente refatorado a vontade.
class ListEditor(TypeEditor):
    """Imgui TypeEditor for editing a LIST value."""

    def __init__(self, config: dict, item_editor: TypeEditor, default_item=None):
        super().__init__(config)
        self.default_item = default_item
        self.item_editor = item_editor
        item_editor.value_getter = lambda obj, i: obj[i]

        def item_setter(obj, i, item):
            obj[i] = item
        item_editor.value_setter = item_setter

    def __call__(self, obj, name: str):
        changed = False
        value = self.value_getter(obj, name)
        if self.draw_start(obj, name):
            changed, value = self.draw_value_editor(obj, name, value)
            self.draw_end(obj, name, changed, value)
        return changed, value

    def draw_start(self, obj, name: str):
        self.update_from_obj(obj, name)
        opened = imgui.tree_node(f"{obj}EditAttr{name}", f"{name} ({len(self.value_getter(obj, name))} items)")
        imgui.set_item_tooltip(self.attr_doc)
        return opened

    def draw_value_editor(self, obj, name: str, value: list):
        changed = False
        size = len(value)
        for i in range(size):
            if i >= len(value):
                break  # required since the X button might remove a item, changing the size of value.
            item = value[i]
            # "start" part
            imgui.push_id(f"{obj}EditAttr{name}ListItem{i}")
            imgui.text(f"#{i}:")
            imgui.same_line()
            # item value editing
            item_changed, new_item = self.item_editor.draw_value_editor(obj, name, item)
            # item handling (move/delete)
            imgui.same_line()
            if imgui.button("^") and i >= 1:
                value[i-1], value[i] = value[i], value[i-1]
                item_changed = False
                changed = True
            imgui.same_line()
            if imgui.button("v") and i < size-1:
                value[i], value[i+1] = value[i+1], value[i]
                item_changed = False
                changed = True
            imgui.same_line()
            if imgui.button("X"):
                value.pop(i)
                item_changed = True
            # "end" part
            elif item_changed:
                value[i] = new_item
            changed = changed or item_changed
            imgui.pop_id()
        if imgui.button("Add Item"):
            value.append(self.default_item)
            changed = True
        return changed, value

    def draw_end(self, obj, name: str, changed: bool, new_value: list):
        if changed:
            self.value_setter(obj, name, new_value)
        imgui.tree_pop()


@TypeDatabase.register_editor_for_type(Vector2)
class Vector2Editor(TypeEditor):
    """Imgui TypeEditor for editing a Vector2 value."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.speed: float = config.get("speed", 1.0)
        self.format: str = config.get("format", "%.2f")
        self.flags: imgui.SliderFlags_ = config.get("flags", 0)
        self.x_range: Vector2 = config.get("x_range", (0, 0))
        self.y_range: Vector2 = config.get("y_range", (0, 0))
        self.add_tooltip_after_value = False
        self.color = Color(0, 0.5, 1, 1)
        self.convert_value_to_type = True

    def draw_value_editor(self, value: Vector2):
        if value is None:
            value = Vector2()
        imgui.push_id("XComp")
        x_changed, value.x = self._component_edit(value.x, self.x_range)
        imgui.set_item_tooltip(f"X component of the Vector2.\n\n{self.attr_doc}")
        imgui.pop_id()
        imgui.same_line()
        imgui.push_id("YComp")
        y_changed, value.y = self._component_edit(value.y, self.y_range)
        imgui.set_item_tooltip(f"Y component of the Vector2.\n\n{self.attr_doc}")
        imgui.pop_id()
        return x_changed or y_changed, value

    def _component_edit(self, value: float, range: tuple[float, float]):
        min, max = range
        if max > min:
            return imgui.slider_float("##value", value, min, max, self.format, self.flags)
        else:
            return imgui.drag_float("##value", value, self.speed, min, max, self.format, self.flags)


def vector2_property(x_range=(0, 0), y_range=(0, 0), format="%.2f", speed=1.0, flags: imgui.SliderFlags_ = 0):
    """Imgui Property attribute for a Vector2 type.

    Behaves the same way as a property, but includes a Vector2Editor object for allowing changing this Vector2's value in imgui.

    Args:
        x_range (tuple[float, float], optional): (min, max) range of possible values for the X component of the vector.
        y_range (tuple[float, float], optional): (min, max) range of possible values for the Y component of the vector.
        format (str, optional): Text format of the value to decorate the control with. Defaults to "%.3". Apparently this needs to be a valid
        python format, otherwise the float control wont work properly.
        speed (float, optional): Speed to apply when changing values. Only applies when dragging the value. Defaults to 1.0.
        flags (imgui.SliderFlags_, optional): Flags for the Slider/Drag float controls. Defaults to imgui.SliderFlags_.none.
    """
    return imgui_property(x_range=x_range, y_range=y_range, format=format, speed=speed, flags=flags)


class NoopEditor(TypeEditor):
    """Imgui TypeEditor for a type that can't be edited.

    This allows editors to exist, and thus provide some other features (such as type color), for types that can't be edited.
    """

    def draw_value_editor[T](self, value: T) -> tuple[bool, T]:
        imgui.text_colored(Colors.yellow, f"Can't edit object '{value}'")
        return False, value


class UnionEditor(TypeEditor):
    """Specialized TypeEditor for UnionType objects (ex.: ``int | float``).

    This editor represents several types (from the union) instead of a single type.
    Values edited with this may be from any one of these "sub-types", and the rendered IMGUI
    controls allows changing the type of the value. If a value's type is not known (such as a None),
    we'll default to the first sub-type.

    Internally, we use other TypeEditors instances for each specific sub-types. The UnionEditor instance
    and its internal "sub-editors" share the same configuration dict. UnionEditor color is the mean color
    of all sub-editors.

    Note! Since this allows changing the type of the value between any of the sub-types, it is expected that
    the sub-types are convertible between themselves.

    This editor class is not registered in the TypeDatabase for any particular kind of (union) type. Instead,
    the TypeDatabase will manually always return a instance of this editor of any union-type that is given.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        database = TypeDatabase()
        self.subeditors: dict[str, TypeEditor] = {}
        colors = []
        for subtype in self.value_subtypes:
            subeditor = database.get_editor(subtype, config)
            self.subeditors[subeditor.type_name()] = subeditor
            colors.append(subeditor.color)
        self.color = Colors.mean_color(colors)

    def type_name(self):
        # When creating a UnionEditor, original_type and value_type should be the same: the union-type object.
        return str(self.value_type)

    def draw_value_editor[T](self, value: T) -> tuple[bool, T]:
        # Get current subeditor for the given value
        subtypes = list(self.subeditors.keys())
        selected_type = self.get_current_value_type(value)
        # Allow used to change the value's type.
        doc = "Type to use with this value"
        changed_type, selected_type = drop_down(selected_type, subtypes, default_doc=doc, drop_flags=imgui.ComboFlags_.width_fit_preview)
        imgui.same_line()
        # Render sub-editor
        subeditor = self.subeditors[selected_type]
        changed, value = subeditor.render_value_editor(value)
        return changed or changed_type, value

    def _check_value_type[T](self, value: T) -> T:
        subeditor = self.subeditors[self.get_current_value_type(value)]
        return subeditor._check_value_type(value)

    def get_current_value_type(self, value):
        """Gets the name of the current type of value, testing it against our possible subtypes.

        Name returned is the type-name which can be used with ``self.subeditors`` to get the editor for that sub-type.

        Args:
            value (any): the value to check

        Returns:
            str: type-name (from our possible subtype names) that matches the given value's type.
        """
        for name, subeditor in self.subeditors.items():
            if isinstance(value, subeditor.value_type):
                return name
        return list(self.subeditors.keys())[0]  # defaults to first subtype


def get_all_renderable_properties(cls: type) -> dict[str, ImguiProperty]:
    """Gets all "Imgui Properties" of a class. This includes properties of parent classes.

    Imgui Properties are properties with an associated ImguiTypeEditor object created with the
    ``@imgui_property(editor)`` and related decorators.

    Args:
        cls (type): the class to get all imgui properties from.

    Returns:
        dict[str,ImguiProperty]: a "property name" => "ImguiProperty object" dict with all imgui properties.
        All editors returned by this will have had their "parent properties" set accordingly.
    """
    return get_all_properties(cls, ImguiProperty)


def render_all_properties(obj, ignored_props: set[str] = None):
    """Renders the KEY:VALUE editors for all imgui properties of the given object.

    This allows seeing and editing the values of all imgui properties in the object.
    See ``get_all_renderable_properties()``.

    Args:
        obj (any): the object to render all imgui properties.
        ignored_props (set[str], optional): a set (or any other object that supports ``X in IGNORED`` (contains protocol)) that indicates
            property names that we should ignore when rendering their editors. This way, if the name of a imgui-property P is in ``ignored_props``,
            its editor will not be rendered. Defaults to None (shows all properties).

    Returns:
        bool: If any property in the object was changed.
    """
    props = get_all_renderable_properties(type(obj))
    changed = False
    for name, prop in props.items():
        if (ignored_props is None) or (name not in ignored_props):
            changed = prop.render_editor(obj) or changed
    return changed
