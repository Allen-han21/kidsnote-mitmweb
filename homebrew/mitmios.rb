class Mitmios < Formula
  include Language::Python::Virtualenv

  desc "Configurable network debugging tool for iOS developers"
  homepage "https://github.com/Allen-han21/mitmios"
  url "https://files.pythonhosted.org/packages/source/m/mitmios/mitmios-0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3.12"

  # Core dependencies
  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.15.1.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/source/P/PyYAML/pyyaml-6.0.2.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
    sha256 "PLACEHOLDER"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "mitmios v#{version}", shell_output("#{bin}/mitmios --version")
  end
end
