# pue
Philips Hue API interface.

## Things you can do
Connect to your bridge:
```
>>> from pue.api import HueAPI
>>> api = HueAPI('10.0.107.80', token='zoop-Yx9b6zHYaw2Rtes6HG9xwr6F6wf3l4us6Am')
```


Enumerate groups:
```
>>> api.groups
{1: <Group: Office (Room)>,
 2: <Group: Bedroom (Room)>,
 3: <Group: Living room (Room)>,
 5: <Group: Custom group for $lights (LightGroup)>,
 6: <Group: Custom group for $group (LightGroup)>}
```


Enumerate lights:
```
>>> api.lights
{4: <Light: Bedroom Ceiling 1>,
 5: <Light: Bedroom Ceiling 2>,
 7: <Light: Office Ceiling 1>,
 8: <Light: Office Ceiling 2>,
 9: <Light: Office Bathroom Ceiling>,
 10: <Light: Living Room Lamp 1>,
 11: <Light: Entryway 1>,
 12: <Light: Entryway 2>,
 13: <Light: Office Lamp>,
 14: <Light: Office Desk 3G>}

>>> api.groups[1].lights
{7: <Light: Office Ceiling 1>,
 8: <Light: Office Ceiling 2>,
 9: <Light: Office Bathroom Ceiling>,
 13: <Light: Office Lamp>,
 14: <Light: Office Desk 3G>}
```


Enumerate scenes:
```
>>> api.scenes
{'exR7mVyhiT0C-PV': <Scene: Relax (GroupScene)>,
 '9BF-y5PLcxy2A10': <Scene: Read (GroupScene)>,
 'bahEMNlGmrrdqWe': <Scene: Concentrate (GroupScene)>,
 'F21yqkk1WZUvfU7': <Scene: Energize (GroupScene)>,
 'WRqxER5xTDx1Ch8': <Scene: Off (GroupScene)>,
 '8kVNOl80ULagV4L': <Scene: Nightlight (GroupScene)>,
 'N2hfZQDzIOPDDqm': <Scene: Last on state (GroupScene)>,
 'DAbleGYGc4pXAAo': <Scene: Rainbow (GroupScene)>}

>>> api.groups[1].scenes
{'exR7mVyhiT0C-PV': <Scene: Relax (GroupScene)>,
 '9BF-y5PLcxy2A10': <Scene: Read (GroupScene)>,
 '8kVNOl80ULagV4L': <Scene: Nightlight (GroupScene)>,
 'DAbleGYGc4pXAAo': <Scene: Rainbow (GroupScene)>}
```


Access lights, groups, and scenes by ID:
```
>>> from pue.lights import Light
>>> Light(api, 14)
<Light: Office Desk 3G>

>>> from pue.groups import Group
>>> Group(api, 1)
<Group: Office (Room)>

>>> from pue.scenes import Scene
>>> Scene(api, 'exR7mVyhiT0C-PV')
<Scene: Relax (GroupScene)>
```


Apply scenes and arbitrary state changes:
```
>>> Scene(api, 'exR7mVyhiT0C-PV').apply()

>>> Group(api, 1).set_state(on=False)

>>> Light(api, 14).set_state(on=True, bri=128)
```

## Things you can sort of do
* Creating groups

## Things you can't do yet
* Authentication (bring your own token)
* Anything involving:
  * Schedules API
  * Sensors API
  * Rules API
  * Configuration API
* Searching light, groups, and scenes by name
* Adding new lights
* Modifying scenes and groups
* Creating scenes
