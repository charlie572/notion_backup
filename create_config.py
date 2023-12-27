from configparser import ConfigParser


def main():
    firefox_path = input("Enter path to firefox executable: ")
    profile_path = input("Enter path to firefox profile: ")

    parser = ConfigParser()
    parser.add_section("firefox")
    parser.set("firefox", "executable", firefox_path)
    parser.set("firefox", "profile", profile_path)

    with open("config.ini", "w") as f:
        parser.write(f)


if __name__ == "__main__":
    main()
