# Maintainer: EchoGate Team

pkgname=echogate
pkgver=1.0.0
pkgrel=2
pkgdesc="Offline spoken-digit challenge for accessibility experiments"
arch=('any')
url="https://github.com/AG064/echogate"
license=('GPL3')
depends=('python' 'python-vosk' 'python-sounddevice' 'espeak-ng' 'tk')
makedepends=('unzip')
source=("echogate.py"
        "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
sha256sums=('33f04f49d68001a092414f59e77fb23f8f3e9fcd615557e22dcf1112d387cec3'
            '30f26242c4eb449f948e42cb302dd7a686cb29a3423a8367f99ff41780942498')
noextract=('vosk-model-small-en-us-0.15.zip')

_vosk_model_name="vosk-model-small-en-us-0.15"

package() {
    # Create installation directories
    install -dm755 "${pkgdir}/opt/echogate"
    install -dm755 "${pkgdir}/opt/echogate/model"
    install -dm755 "${pkgdir}/usr/bin"

    # Install the verified offline model. Python libraries are managed by pacman.
    unzip -oq "${srcdir}/vosk-model-small-en-us-0.15.zip" -d "${srcdir}"
    cp -r "${srcdir}/${_vosk_model_name}"/* "${pkgdir}/opt/echogate/model/"

    # Install main script to /opt/echogate and symlink to /usr/bin
    install -Dm755 "${srcdir}/echogate.py" "${pkgdir}/opt/echogate/echogate.py"
    ln -s /opt/echogate/echogate.py "${pkgdir}/usr/bin/echogate"
}
