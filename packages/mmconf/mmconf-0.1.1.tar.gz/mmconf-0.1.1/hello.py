from mmconf import Config


def main():
    config = Config.fromfile(r"F:\JaxAILab\mmconf\configs\toy.py")
    print(config.to_dict())


if __name__ == "__main__":
    main()
