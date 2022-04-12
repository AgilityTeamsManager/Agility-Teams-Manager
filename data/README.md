# Agility Teams Manager - Teams ranking in agility competitions

## `data/`  - Saved data

### `sessions.dat` - Sessions list

This contains a map between session IDs (UUIDs) and user - competition ID.

#### Structure

{
    Session ID: (User mail, competition ID)
    ...
}

#### Example

```python
{
    "063c6393-32e3-40a1-8d23-f66aec613f70": ("alexcode228@gmail.com", 10956),
    "1f8a14df-9282-4e8b-86e9-e6cd74454a50": ("progesco.teams@gmail.com", 11293),
}
```
