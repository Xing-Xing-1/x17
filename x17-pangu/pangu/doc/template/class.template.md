- **Documentation**
    - **Name**: `[ClassName]`
    - **Type**
        - **Functionalities**: `["Model", "VO", "DTO", "Service", "Controller", "Adapter", "Helper", "Config", "Exception", "Repository"]`
        - **Structures**: `["Concrete", "Abstract", "Base", "Mixin", "Singleton", "Interface", "Protocol"]`
        - **Roles**: `["Factory", "Strategy", "Command", "State", "Template Method", "Decorator", "Composite", "Proxy", "Observer", "Visitor"]`
    - **Parent**
        - **Parents**: `["BaseClass1", "SomeInterface"]`
    - **Child**
        - **Children**: `["SubClassA", "SubClassB"]`
    - **Ref**
        - **Refs**: `["ExternalModule", "AWSClient", "SomeMethod"]`
    - **Desc**
        - `One-sentence or paragraph description of what this class is and does.`
    - **Usage**
        ```python
        # Example usage
        instance = ClassName(param1=value)
        instance.do_something()
        ```
    - **Thread Safe**: `true | false`
    - **Mutable**: `true | false`
    - **Lifecycle**: `["Singleton", "PerCall", "LongLived", "Stateless", "RequestScoped", "Transient"]`
    - **Design Patterns**
        - `["Value Object", "Factory", "Strategy", "Adapter", "Facade", "Proxy", "Command", "Template Method", "Decorator", "Observer", "Composite"]`
    - **Permissions**
        - `["s3:GetObject", "ec2:DescribeInstances", "file:write", "custom:UserScopeCheck"]`
    - **Deprecation**
        - `true | false`
        - **ReplacedBy**: `[NewMethod or ClassName]`
    - **Module**: `path.to.module`
    - **Author**: `Your Name`

- **Class Parameters**
    - `param_name`
        - **Type**: `[int | float | str | bool | list | dict | Enum | Callable | CustomClass]`
        - **Desc**: `What this parameter represents`
        - **Optional**: `true | false`
        - **Default**: `[default_value]`

- **Attributes**
    - `attribute_name`
        - **Type**: `[int | float | str | list | dict | object | Callable | Class]`
        - **Desc**: `What this attribute stores or tracks`

- **Instance Methods**
    - `method_name`
        - **Params**
            - `param_name`: `[type]`, `Purpose of this parameter`
        - **Returns**
            - `[type]`: `Description of return value`
        - **Error Handling**
            - `[ExceptionType]`: `When and why it is raised`
        - **Side Effects**
            - `["modifies self", "calls remote API", "writes to disk", "logs", "none"]`
        - **Related Methods**
            - `["other_method_name", "base_class_method"]`

- **Static Methods**
    - `method_name`
        - **Params**
            - `param_name`: `[type]`, `Explanation`
        - **Returns**
            - `[type]`: `What the static method returns`
        - **Related Methods**
            - `["related_method_name"]`

- **Class Methods**
    - `method_name`
        - **Params**
            - `param_name`: `[type]`, `Explanation`
        - **Returns**
            - `[type]`: `What the class method returns`
        - **Related Methods**
            - `["alternative_constructor", "deserialization helper"]`