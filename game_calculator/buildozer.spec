[app]
title = Game Calculator
package.name = gamecalculator
package.domain = org.gamecalculator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0.0
requirements = python3,kivy==2.1.0

orientation = portrait

android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 26

android.accept_sdk_license = True

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2