import json
from pathlib import Path
from typing import List

from src.config import STEAM_WALLPAPER_PATH
from src.models.wallpaper import (ComboOptions, Wallpaper,
                                  WallpaperBooleanProperty,
                                  WallpaperColorProperty,
                                  WallpaperComboProperty,
                                  WallpaperFileProperty, WallpaperProperty,
                                  WallpaperPropertyType,
                                  WallpaperSliderProperty,
                                  WallpaperTextinputProperty, WallpaperType)


def load_wallpapers(dir: Path = STEAM_WALLPAPER_PATH) -> List[Wallpaper]:
    if not dir.exists():
        return []

    wallpapers: List[Wallpaper] = []

    for wallpaper_folder in dir.iterdir():
        if not wallpaper_folder.is_dir():
            continue

        project_path = wallpaper_folder / "project.json"
        if not project_path.exists():
            continue

        project_file = open(str(project_path), "r")
        try:
            project = json.load(project_file)
        except Exception as e:
            print(f"[WallpaperLoader] Error parsing json: {e}")
            project_file.close()
            continue

        wallpaper = Wallpaper()
        if project["contentrating"] is str:
            wallpaper.contentrating = project["contentrating"]

        if project["file"] is str:
            wallpaper.file = wallpaper_folder / project["file"]

        if project["general"] and project["general"]["properties"] is dict:
            properties: dict[str, WallpaperPropertyType] = {}

            for _, (property_name, property_object) in project["general"]["properties"]:
                if not property_object["type"] is str:
                    continue

                if not property_object["text"] is str:
                    continue

                match property_object["type"]:
                    case "bool":
                        if not property_object["value"] is bool:
                            print(
                                f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                            )
                            continue

                        property = WallpaperBooleanProperty(
                            property_object["text"],
                            property_object["type"],
                            property_object["value"],
                        )

                        properties[property_name] = property

                    case "slider":
                        if (
                            not property_object["min"] is int
                            or not property_object["max"] is int
                            or not property_object["value"] is int
                            or not property_object["editable"] is bool
                        ):
                            print(
                                f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                            )
                            continue

                        property = WallpaperSliderProperty(
                            property_object["text"],
                            property_object["type"],
                            property_object["min"],
                            property_object["max"],
                            property_object["value"],
                            property_object["editable"],
                        )

                        properties[property_name] = property

                    case "color":
                        if not property_object["value"] is str:
                            continue

                        property = WallpaperColorProperty(
                            property_object["text"],
                            property_object["type"],
                            property_object["value"],
                        )

                        properties[property_name] = property

                    case "file":
                        property = WallpaperFileProperty(
                            property_object["text"], property_object["type"]
                        )

                        properties[property_name] = property

                    case "combo":
                        if (
                            not property_object["options"] is list
                            or not property_object["value"] is int
                        ):
                            print(
                                f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                            )
                            continue

                        combo_options: List[ComboOptions] = []
                        for option in property_object["options"]:
                            if not option["label"] is str or not option["value"] is int:
                                continue

                            combo_option = ComboOptions(
                                option["label"], option["value"]
                            )

                            combo_options.append(combo_option)

                        property = WallpaperComboProperty(
                            property_object["text"],
                            property_object["type"],
                            combo_options,
                            property_object["value"],
                        )

                        properties[property_name] = property

                    case "textinput":
                        if not property_object["value"] is str:
                            print(
                                f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                            )
                            continue

                        property = WallpaperTextinputProperty(
                            property_object["text"],
                            property_object["type"],
                            property_object["value"],
                        )

                        properties[property_name] = property

                    case type:
                        print(
                            f"[WallpaperLoader] Warning: property type {type} not implemented yet"
                        )
                        continue

            wallpaper.properties = properties
            if project["monetization"] is bool:
                wallpaper.monetization = project["monetization"]

            if project["preview"] is str:
                wallpaper.preview = wallpaper_folder / project["preview"]

            if project["tags"] is list:
                tags: List[str] = []

                for tag in project["tags"]:
                    if tag is str:
                        tags.append(str(tag))  # pyright is scaring me...

                wallpaper.tags = tags

            if not project["type"] is str:
                print(
                    f"[WallpaperLoader] Error: Wallpaper {wallpaper_folder} doesn't represent a type"
                )
                continue

            try:
                wallpaper.type = WallpaperType(project["type"])
            except Exception:
                print(
                    f"[WallpaperLoader] Error: Wallpaper {wallpaper_folder} type ({project["type"]}) is unappropriable"
                )
                continue

            wallpapers.append(wallpaper)

        project_file.close()

    return wallpapers


def print_wallpapers(wallpapers: List[Wallpaper]):
    for wallpaper in wallpapers:
        properties = ", ".join(wallpaper.properties.keys())
        tags = ", ".join(wallpaper.tags)
        print(f"""
            Wallpaper {wallpaper.type}
                File {wallpaper.file}
                Properties {properties}
                monetization {"true" if wallpaper.monetization else "false"}
                preview {wallpaper.preview}
                tags {tags}
                
        """)
