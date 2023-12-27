from configparser import ConfigParser


def main():
    firefox_path = input("Enter path to firefox executable: ")
    profile_path = input("Enter path to firefox profile: ")
    destination = input("Enter destination for notion exports: ")
    num_exports_to_keep = int(input("Enter number of notion exports to keep: "))

    parser = ConfigParser()

    parser.add_section("firefox")
    parser.set("firefox", "executable", firefox_path)
    parser.set("firefox", "profile", profile_path)

    parser.add_section("exports")
    parser.set("exports", "directory", destination)
    parser.set("exports", "num_to_keep", str(num_exports_to_keep))

    with open("config.ini", "w") as f:
        parser.write(f)


if __name__ == "__main__":
    main()
