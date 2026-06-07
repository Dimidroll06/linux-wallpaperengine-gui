import json
from pathlib import Path
from typing import List

from src.config import STEAM_WALLPAPER_PATH
from src.models.wallpaper import (ComboOptions, Wallpaper,
                                  WallpaperBooleanProperty,
                                  WallpaperColorProperty,
                                  WallpaperComboProperty,
                                  WallpaperFileProperty, WallpaperPropertyType,
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

        try:
            with open(project_path, "r") as project_file:
                project = json.load(project_file)
        except Exception as e:
            print(f"[WallpaperLoader] Error parsing json: {e}")
            continue

        wallpaper = Wallpaper()

        contentrating = project.get("contentrating")
        if isinstance(contentrating, str):
            wallpaper.contentrating = contentrating

        file_name = project.get("file")
        if isinstance(file_name, str):
            wallpaper.file = wallpaper_folder / file_name

        general = project.get("general")
        if isinstance(general, dict):
            properties_data = general.get("properties")
            if isinstance(properties_data, dict):
                properties: dict[str, WallpaperPropertyType] = {}

                for property_name, property_object in properties_data.items():
                    if not isinstance(property_object, dict):
                        continue

                    prop_type = property_object.get("type")
                    prop_text = property_object.get("text")

                    if not isinstance(prop_type, str) or not isinstance(prop_text, str):
                        continue

                    match prop_type:
                        case "bool":
                            prop_value = property_object.get("value")
                            if not isinstance(prop_value, bool):
                                print(
                                    f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                                )
                                continue

                            property = WallpaperBooleanProperty(
                                prop_text,
                                prop_type,
                                prop_value,
                            )
                            properties[property_name] = property

                        case "slider":
                            prop_min = property_object.get("min")
                            prop_max = property_object.get("max")
                            prop_value = property_object.get("value")
                            prop_editable = property_object.get("editable")

                            if (
                                not isinstance(prop_min, int)
                                or not isinstance(prop_max, int)
                                or not isinstance(prop_value, int)
                                or not isinstance(prop_editable, bool)
                            ):
                                print(
                                    f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                                )
                                continue

                            property = WallpaperSliderProperty(
                                prop_text,
                                prop_type,
                                prop_min,
                                prop_max,
                                prop_value,
                                prop_editable,
                            )
                            properties[property_name] = property

                        case "color":
                            prop_value = property_object.get("value")
                            if not isinstance(prop_value, str):
                                continue

                            property = WallpaperColorProperty(
                                prop_text,
                                prop_type,
                                prop_value,
                            )
                            properties[property_name] = property

                        case "file":
                            property = WallpaperFileProperty(prop_text, prop_type)
                            properties[property_name] = property

                        case "combo":
                            prop_options = property_object.get("options")
                            prop_value = property_object.get("value")

                            if not isinstance(prop_options, list) or not isinstance(
                                prop_value, int
                            ):
                                print(
                                    f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                                )
                                continue

                            combo_options: List[ComboOptions] = []
                            for option in prop_options:
                                if not isinstance(option, dict):
                                    continue

                                option_label = option.get("label")
                                option_value = option.get("value")

                                if not isinstance(option_label, str) or not isinstance(
                                    option_value, int
                                ):
                                    continue

                                combo_option = ComboOptions(option_label, option_value)
                                combo_options.append(combo_option)

                            property = WallpaperComboProperty(
                                prop_text,
                                prop_type,
                                combo_options,
                                prop_value,
                            )
                            properties[property_name] = property

                        case "textinput":
                            prop_value = property_object.get("value")
                            if not isinstance(prop_value, str):
                                print(
                                    f"[WallpaperLoader] Warning: property {property_name} for wallpaper {wallpaper_folder} is misstyped"
                                )
                                continue

                            property = WallpaperTextinputProperty(
                                prop_text,
                                prop_type,
                                prop_value,
                            )
                            properties[property_name] = property

                        case _:
                            print(
                                f"[WallpaperLoader] Warning: property type {prop_type} not implemented yet"
                            )
                            continue

                wallpaper.properties = properties

        monetization = project.get("monetization")
        if isinstance(monetization, bool):
            wallpaper.monetization = monetization

        preview_name = project.get("preview")
        if isinstance(preview_name, str):
            wallpaper.preview = wallpaper_folder / preview_name

        tags_data = project.get("tags")
        if isinstance(tags_data, list):
            tags: List[str] = []
            for tag in tags_data:
                if isinstance(tag, str):
                    tags.append(tag)
            wallpaper.tags = tags

        wallpaper_type = project.get("type")
        if not isinstance(wallpaper_type, str):
            print(
                f"[WallpaperLoader] Error: Wallpaper {wallpaper_folder} doesn't represent a type"
            )
            continue

        try:
            wallpaper.type = WallpaperType(wallpaper_type)
        except Exception:
            print(
                f"[WallpaperLoader] Error: Wallpaper {wallpaper_folder} type ({wallpaper_type}) is unappropriable"
            )
            continue

        wallpapers.append(wallpaper)

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
