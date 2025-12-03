# Maintainer: EchoGate Team

pkgname=echogate
pkgver=1.0.0
pkgrel=1
pkgdesc="Voice-based authentication using speech recognition"
arch=('any')
url="https://github.com/AG064/echogate"
license=('GPL3')
depends=('python' 'python-sounddevice' 'espeak-ng' 'tk')
makedepends=('python-pip' 'unzip')
source=("echogate.py"
        "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
sha256sums=('SKIP'
            'SKIP')
noextract=('vosk-model-small-en-us-0.15.zip')

_vosk_model_name="vosk-model-small-en-us-0.15"

package() {
    # Create installation directories
    install -dm755 "${pkgdir}/opt/echogate"
    install -dm755 "${pkgdir}/opt/echogate/libs"
    install -dm755 "${pkgdir}/opt/echogate/model"
    install -dm755 "${pkgdir}/usr/bin"

    # Install vosk to custom libs directory
    pip install vosk --target="${pkgdir}/opt/echogate/libs" --no-deps --ignore-installed --no-cache-dir

    # Extract and install the vosk model
    unzip -q "${srcdir}/vosk-model-small-en-us-0.15.zip" -d "${srcdir}"
    cp -r "${srcdir}/${_vosk_model_name}"/* "${pkgdir}/opt/echogate/model/"

    # Install main script to /opt/echogate and symlink to /usr/bin
    install -Dm755 "${srcdir}/echogate.py" "${pkgdir}/opt/echogate/echogate.py"
    ln -s /opt/echogate/echogate.py "${pkgdir}/usr/bin/echogate"
}
