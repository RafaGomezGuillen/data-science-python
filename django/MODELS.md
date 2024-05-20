# Creating a Python model

## Fields

### Char Field

- `max_length`: Specifies the maximum length of the character field.

- `validators`: Validators are functions that validate the input data. In both examples, MinLengthValidator is used to ensure that the length of the input value is at least 3 characters long.

```py
from django.core.validators import MinLengthValidator

class Model(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(
        3, "The task must be between 3 and 200 characters long.")])
```

### Char Field

- `null` and `blank`: Determine whether the field can be null (null=True) and whether it is allowed to be blank (blank=True).

```py
class Model(models.Model):
    description = models.TextField(null=True, blank=True, validators=[MinLengthValidator(
        3, "The task must be at least 3 characters long.")])
```

### Boolean Field

- `default`: Specifies the default value for the field if no value is provided.

```py
class Model(models.Model):
    complete = models.BooleanField(default=False)
```

### Date Time Field

- `auto_now_add`: This attribute, when set to True, automatically sets the field to the current date and time when the object is first created.

```py
class Model(models.Model):
    created = models.DateTimeField(auto_now_add=True)
```

### Choices

```py
class Model(models.Model):
    RESOURCE_TYPE = [
            ('HU', 'Human'),
            ('FI', 'Finantial'),
            ('MA', 'Material'),
            ('TE', 'Technical'),
        ]
    
    type = models.CharField(max_lenght=2, choices=RESOURCE_TYPE, default='MA')
```