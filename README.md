
Network Location workflow for Alfred
====================================

View and change your network location from [Alfred][alfred].

![][screenshot]


## Installation ##

Grab the latest version from the [releases page][releases].

**Note:** If you're still using Alfred 2, download [v1.0][v1.0]. Later versions are only compatible with Alfred 3.


## Usage ##

- `netloc [<query>]` — Show list of network locations filtered by `<query>` if one is specified
	+ `↩` — Activate selected network location
	+ `⌘+↩` — Open Network Preferences


## Licence ##

This workflow is released under the [MIT Licence][mit].


## Changelog ##

- [v2.0][v2.0] — 2018-03-31
    - Add built-in update mechanism
    - Use `scselect` instead of `networksetup` (no need to enter password)
    - Smarter caching
- [v1.0][v1.0] — 2014-06-18
    - Initial release


[alfred]: https://www.alfredapp.com/
[v1.0]: https://github.com/deanishe/alfred-network-location/releases/tag/v1.0
[v2.0]: https://github.com/deanishe/alfred-network-location/releases/tag/v2.0
[releases]: https://github.com/deanishe/alfred-network-location/releases
[screenshot]: https://raw.githubusercontent.com/deanishe/alfred-network-location/master/screenshot.png
[mit]: http://opensource.org/licenses/MIT
