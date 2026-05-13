[app]

title = EMI Calculator

package.name = emicalculator
package.domain = org.emi

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1

orientation = portrait

fullscreen = 0

android.api = 31
android.minapi = 21
android.sdk = 24
android.ndk = 25b

android.accept_sdk_license = True

android.permissions = INTERNET

log_level = 2

[buildozer]

warn_on_root = 0
