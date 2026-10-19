from nbhelp import NB, T

NOTEBOOK = NB(
    "classes", "Classes for data records", 2, ["2.3.1", "2.3.2", "2.3.3"],
    "Attributes and methods, __eq__ and __repr__, inheritance, composition and properties.",
    """
    `Sensor` is a base class: every sensor has a `name`, `describe()` builds a line of text,
    and subclasses supply `read()`.
    """,
    """
    class Sensor:
        def __init__(self, name):
            self.name = name

        def read(self):
            raise NotImplementedError("subclasses implement read()")

        def describe(self):
            return f"{self.name}: {self.read()}"
    """,
    [
        T("reading", "Attributes and a method",
          """
          Write a class `Reading` whose `__init__` takes `sensor` and `value` and stores them as attributes of the same names.
          Add a method `is_high(limit=22)` that returns `True` when `value` is above `limit`.
          """,
          """
          class Reading:
              pass
          """,
          """
          class Reading:
              def __init__(self, sensor, value):
                  self.sensor = sensor
                  self.value = value

              def is_high(self, limit=22):
                  return self.value > limit
          """,
          """
          r = Reading("t1", 23.0)
          assert r.sensor == "t1" and r.value == 23.0, "store sensor and value as attributes (self.sensor = sensor)"
          assert r.is_high() is True, "23.0 is above the default limit of 22"
          assert Reading("t2", 10).is_high() is False, "10 is not above 22"
          assert Reading("t3", 10).is_high(limit=5) is True, "is_high should use the limit passed in"
          assert Reading("t4", 22).is_high() is False, "a value equal to the limit is not above it"
          """,
          ["Methods take `self` first; attributes are set with `self.name = value` inside `__init__`."]),

        T("equality", "Equality versus identity",
          """
          Write a class `Point` with attributes `x` and `y` where:

          - `Point(1, 2) == Point(1, 2)` is `True` (same coordinates), yet the two are different objects (`is` gives `False`);
          - `repr(Point(1, 2))` is `"Point(1, 2)"`;
          - comparing a `Point` with something that is not a `Point` returns `False` rather than raising.
          """,
          """
          class Point:
              def __init__(self, x, y):
                  self.x = x
                  self.y = y
          """,
          """
          class Point:
              def __init__(self, x, y):
                  self.x = x
                  self.y = y

              def __eq__(self, other):
                  if not isinstance(other, Point):
                      return NotImplemented
                  return (self.x, self.y) == (other.x, other.y)

              def __repr__(self):
                  return f"Point({self.x!r}, {self.y!r})"
          """,
          """
          a, b = Point(1, 2), Point(1, 2)
          assert a == b, "two Points with the same coordinates should be equal: define __eq__"
          assert a is not b, "they are still two separate objects"
          assert Point(1, 2) != Point(2, 1), "different coordinates should not be equal"
          assert repr(a) == "Point(1, 2)", f"repr gave {repr(a)!r}"
          try:
              result = a == "Point(1, 2)"
          except Exception as exc:
              raise AssertionError(f"comparing with a string raised {type(exc).__name__}; return NotImplemented for other types")
          assert result is False, "a Point should not equal a string"
          """,
          ["Without `__eq__`, `==` falls back to identity, so two separate objects are never equal.",
           "Returning `NotImplemented` from `__eq__` lets Python try the other side and then fall back to `False`."]),

        T("inherit", "Subclasses and super()",
          """
          Write two subclasses of `Sensor`:

          - `Thermometer(name, celsius)`, whose `read()` returns the temperature with one decimal and ` C`, e.g. `"21.5 C"`;
          - `Hygrometer(name, pct)`, whose `read()` returns e.g. `"40%"`.

          Call `super().__init__(name)` rather than setting `name` yourself; `describe()` is inherited unchanged.
          """,
          """
          class Thermometer(Sensor):
              pass


          class Hygrometer(Sensor):
              pass
          """,
          """
          class Thermometer(Sensor):
              def __init__(self, name, celsius):
                  super().__init__(name)
                  self.celsius = celsius

              def read(self):
                  return f"{self.celsius:.1f} C"


          class Hygrometer(Sensor):
              def __init__(self, name, pct):
                  super().__init__(name)
                  self.pct = pct

              def read(self):
                  return f"{self.pct}%"
          """,
          """
          t = Thermometer("lab", 21.46)
          h = Hygrometer("lab", 40)
          assert isinstance(t, Sensor) and isinstance(h, Sensor), "both classes should inherit from Sensor"
          assert t.name == "lab", "the name should be stored by Sensor.__init__ (call super().__init__(name))"
          assert t.read() == "21.5 C", f"Thermometer.read() gave {t.read()!r}, expected '21.5 C'"
          assert h.read() == "40%", f"Hygrometer.read() gave {h.read()!r}, expected '40%'"
          assert [s.describe() for s in (t, h)] == ["lab: 21.5 C", "lab: 40%"], "describe() should come from Sensor and call each subclass's read()"
          assert "describe" not in vars(Thermometer) and "describe" not in vars(Hygrometer), "inherit describe() instead of redefining it"
          """,
          ["Format with one decimal: `f\"{value:.1f}\"`.",
           "The same `describe()` call gives different text for each subclass: that is polymorphism."]),

        T("compose", "Composition: a station holds sensors",
          """
          Write a class `Station(name)` that **has** sensors (composition, not inheritance):

          - `add(sensor)` stores a sensor;
          - `len(station)` gives the number of sensors;
          - `report()` returns the list of each sensor's `describe()` text, in the order they were added.

          Two stations must not share their sensors.
          """,
          """
          class Station:
              sensors = []

              def __init__(self, name):
                  self.name = name

              def add(self, sensor):
                  self.sensors.append(sensor)
          """,
          """
          class Station:
              def __init__(self, name):
                  self.name = name
                  self.sensors = []

              def add(self, sensor):
                  self.sensors.append(sensor)

              def __len__(self):
                  return len(self.sensors)

              def report(self):
                  return [s.describe() for s in self.sensors]
          """,
          """
          class Fixed(Sensor):
              def __init__(self, name, text):
                  super().__init__(name)
                  self.text = text

              def read(self):
                  return self.text

          roof = Station("roof")
          roof.add(Fixed("a", "ok"))
          roof.add(Fixed("b", "low"))
          cellar = Station("cellar")
          assert len(cellar) == 0, "a new station should have no sensors: a list defined on the class is shared by every instance, so create it in __init__"
          assert len(roof) == 2, "len() should count the sensors (define __len__)"
          assert roof.report() == ["a: ok", "b: low"], f"report() gave {roof.report()}"
          assert not isinstance(roof, Sensor), "a Station has sensors; it is not a sensor itself"
          """,
          ["A list written in the class body is a class attribute, shared by all instances. Create `self.sensors = []` in `__init__`.",
           "`len(obj)` calls `obj.__len__()`."]),

        T("property", "A validated property",
          """
          Write a class `Temperature(celsius)` with:

          - a property `celsius` whose setter raises `ValueError` for values below -273.15 (also when the object is created);
          - a read-only property `fahrenheit` computed as `celsius * 9 / 5 + 32`.
          """,
          """
          class Temperature:
              def __init__(self, celsius):
                  self.celsius = celsius
                  self.fahrenheit = celsius * 9 / 5 + 32
          """,
          """
          class Temperature:
              def __init__(self, celsius):
                  self.celsius = celsius

              @property
              def celsius(self):
                  return self._celsius

              @celsius.setter
              def celsius(self, value):
                  if value < -273.15:
                      raise ValueError("below absolute zero")
                  self._celsius = value

              @property
              def fahrenheit(self):
                  return self.celsius * 9 / 5 + 32
          """,
          """
          t = Temperature(100)
          assert t.fahrenheit == 212, f"100 C should be 212 F, got {t.fahrenheit}"
          t.celsius = 0
          assert t.fahrenheit == 32, "fahrenheit should follow celsius when celsius changes (compute it in a property)"
          try:
              t.celsius = -300
          except ValueError:
              pass
          else:
              raise AssertionError("setting celsius to -300 should raise ValueError")
          try:
              Temperature(-500)
          except ValueError:
              pass
          else:
              raise AssertionError("Temperature(-500) should raise ValueError: assign through the property in __init__")
          try:
              t.fahrenheit = 50
          except AttributeError:
              pass
          else:
              raise AssertionError("fahrenheit should be read-only (a property with no setter)")
          """,
          ["`@property` makes a method read like an attribute; `@celsius.setter` runs on assignment.",
           "Store the value under another name (`self._celsius`) or the setter would call itself forever."]),
    ],
)
