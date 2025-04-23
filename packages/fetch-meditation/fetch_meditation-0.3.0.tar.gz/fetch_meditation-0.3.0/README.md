# Fetch Meditation Py

* Python library for reading and parsing daily meditations

### Basic Usage
```py
from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.jft import Jft

settings = JftSettings(JftLanguage.Russian)
jft_instance = Jft.get_instance(settings)
jft_entry = jft_instance.fetch()

print(jft_entry.quote)
```
