import subprocess
import re
import requests
import platform as sys_platform

class ChromeDriverManager:
    @classmethod
    def get_chrome_version(cls):
        try:
            output = subprocess.check_output(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                shell=True, stderr=subprocess.DEVNULL, text=True
            )
            match = re.search(r"version\s+REG_SZ\s+([^\s]+)", output)
            if match:
                return match.group(1)
            else:
                raise ValueError("Chrome version not found in registry output.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to get Chrome version.") from e

    @classmethod
    def get_latest_chromedriver(cls, version: str = None, dest_folder: str = None, platform: str = None):
        try:
            response = requests.get(
                "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
            )
            response.raise_for_status()
            data = response.json()

            chrome_version = version or cls.get_chrome_version().split(".")[0]

            if platform is None:
                platform = "win64" if sys_platform.system() == "Windows" else "mac-arm64" if sys_platform.machine() == "arm64" else "linux64"

            for item in data["versions"]:
                if chrome_version in item["version"]:
                    urls = [
                        d["url"] for d in item["downloads"]["chromedriver"]
                        if d["platform"] == platform
                    ]
                    if urls:
                        return urls[-1]
                    else:
                        raise RuntimeError(f"No matching ChromeDriver URL for platform '{platform}'")
            raise RuntimeError(f"No ChromeDriver found for version {chrome_version}")
        except requests.RequestException as e:
            raise RuntimeError("Failed to fetch ChromeDriver versions.") from e
