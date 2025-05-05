# 🦥 SiteSloth: A Domain-based Internet Throttler

SiteSloth is a tool designed to throttle internet speed for specific domains using `mitmproxy`. It allows users to specify websites and throttle speeds, providing a controlled browsing experience.

## Features

- Throttle internet speed for specified domains.
- Secure access with an admin passcode.
- Dynamic update of throttled websites and speeds.
- Cross-platform support (macOS, Linux, Windows).

## Installation

### Prerequisites

- **mitmproxy**: Download and install from [mitmproxy.org](https://mitmproxy.org/downloads/#12.0.0/).

### Download and Setup

1. **Download the ZIP file**:
   - Go to the repository page on GitHub.
   - Click on the "Code" button and select "Download ZIP".
   - Extract the ZIP file to your desired location.

2. **Install mitmproxy**:
   - Follow the instructions on [mitmproxy.org](https://mitmproxy.org/downloads/#12.0.0/) to download and install the appropriate version for your system.

## Installing mitmproxy Certificate

### macOS

1. **Locate mitmproxy’s certificate**:
   - Default location: `~/.mitmproxy/mitmproxy-ca-cert.pem`
   - If missing, run `mitmproxy` or `mitmdump` once to generate.

2. **Open Keychain Access**:
   - Search in Spotlight and open.
   - Select “System” keychain.

3. **Import the certificate**:
   - File → Import Items…
   - Navigate to `~/.mitmproxy/mitmproxy-ca-cert.pem` and open.

4. **Set the certificate to “Always Trust”**:
   - Find mitmproxy in the System keychain.
   - Double-click, expand “Trust”, set “When using this certificate” to “Always Trust”.

5. **Verify**:
   - Test by visiting an HTTPS site via mitmproxy in Safari or Chrome.

### Linux

1. **Locate mitmproxy's certificate**:
   - Default location: `~/.mitmproxy/mitmproxy-ca-cert.pem`

2. **Install certificate for Firefox**:
   - Open Firefox → Preferences → Privacy & Security → Certificates → View Certificates.
   - Import `~/.mitmproxy/mitmproxy-ca-cert.pem`.

3. **Install certificate into system-wide store**:
   - **Ubuntu/Debian**:
     ```bash
     sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
     sudo update-ca-certificates
     ```
   - **Fedora/RHEL/CentOS**:
     ```bash
     sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /etc/pki/ca-trust/source/anchors/mitmproxy-ca-cert.pem
     sudo update-ca-trust
     ```

4. **Verify**:
   - Test with `curl https://example.com --proxy http://localhost:8080`.

### Windows

1. **Download mitmproxy**:
   - Download the Windows installer from [mitmproxy.org](https://mitmproxy.org/downloads/).

2. **Generate and install the mitmproxy certificate**:
   - Run `mitmdump` to generate the certificate at `C:\Users\<YourUser>\.mitmproxy\mitmproxy-ca-cert.pem`.

3. **Import the certificate into Windows Trusted Root**:
   - Open “Manage Computer Certificates” (certmgr.msc).
   - Import the certificate into Trusted Root Certification Authorities.

4. **Verify installation**:
   - Test mitmproxy by intercepting HTTPS traffic in a browser.

## Usage

1. **Run SiteSloth**:
   - **macOS**: Double-click `SiteSlothMac.command`.
   - **Linux**: Run `SiteSlothLinux.sh` in a terminal.
   - **Windows**: Double-click `SiteSlothWindows.py`.

2. Follow the prompts to enter websites and throttle speed.

3. Use commands like `exit`, `website`, `speed`, and `help` to manage the throttling.

## Important Notes

- Ensure the certificate is installed in the correct store and set to "Always Trust".
- Firefox requires separate certificate import.
- Some applications may not honor system certificates.

## Contributing

We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Submit a pull request to the main repository.
Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## Contact

For questions or support, please open an issue on the GitHub repository or contact me at [goharwah786@gmail.com].
