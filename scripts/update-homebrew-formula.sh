#!/bin/bash
set -euo pipefail

# Update Homebrew formula with correct URLs and SHA256 hashes
# Usage: ./scripts/update-homebrew-formula.sh <version>
# Example: ./scripts/update-homebrew-formula.sh 0.1.0

VERSION="${1:?Usage: $0 <version>}"
FORMULA="homebrew/mitmios.rb"
TAP_REPO="$HOME/Dev/personal/homebrew-mitmios"

echo "Updating Homebrew formula for mitmios v${VERSION}"
echo ""

# Function to get SHA256 of a PyPI package
get_pypi_sha256() {
    local package="$1"
    local version="$2"
    python3 -c "
import json, urllib.request
url = f'https://pypi.org/pypi/${package}/${version}/json'
data = json.loads(urllib.request.urlopen(url).read())
for f in data['urls']:
    if f['packagetype'] == 'sdist':
        print(f['digests']['sha256'])
        break
" 2>/dev/null
}

echo "[1/4] Fetching SHA256 for mitmios ${VERSION}..."
MITMIOS_SHA=$(get_pypi_sha256 "mitmios" "$VERSION")
if [ -z "$MITMIOS_SHA" ]; then
    echo "  Warning: mitmios ${VERSION} not found on PyPI yet"
    MITMIOS_SHA="PLACEHOLDER_SHA256"
else
    echo "  SHA256: ${MITMIOS_SHA:0:16}..."
fi

echo "[2/4] Generating formula..."

cat > "$FORMULA" << RUBY
class Mitmios < Formula
  include Language::Python::Virtualenv

  desc "Configurable network debugging tool for iOS developers"
  homepage "https://github.com/Allen-han21/mitmios"
  url "https://files.pythonhosted.org/packages/source/m/mitmios/mitmios-${VERSION}.tar.gz"
  sha256 "${MITMIOS_SHA}"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "mitmios v#{version}", shell_output("#{bin}/mitmios --version")
  end
end
RUBY

echo "  Generated: ${FORMULA}"

echo "[3/4] Checking tap repo..."
if [ -d "$TAP_REPO" ]; then
    echo "  Copying to tap repo: ${TAP_REPO}"
    cp "$FORMULA" "$TAP_REPO/Formula/mitmios.rb"
    echo "  Done. Remember to commit and push the tap repo."
else
    echo "  Tap repo not found at: ${TAP_REPO}"
    echo "  To set up the tap repo:"
    echo ""
    echo "    mkdir -p ~/Dev/personal/homebrew-mitmios/Formula"
    echo "    cd ~/Dev/personal/homebrew-mitmios"
    echo "    git init"
    echo "    cp ${FORMULA} Formula/mitmios.rb"
    echo "    git add . && git commit -m 'Add mitmios formula v${VERSION}'"
    echo "    gh repo create Allen-han21/homebrew-mitmios --public --source=. --push"
fi

echo ""
echo "[4/4] Install instructions:"
echo ""
echo "  brew tap Allen-han21/mitmios"
echo "  brew install mitmios"
echo ""
echo "Done."
