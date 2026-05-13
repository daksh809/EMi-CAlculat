[app]

title = EMI Calculator

package.name = emicalculator
package.domain = org.emi

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 21

android.permissions = INTERNET

log_level = 2

[buildozer]

warn_on_root = 0
