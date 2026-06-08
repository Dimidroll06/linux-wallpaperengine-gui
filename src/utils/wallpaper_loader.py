import json
import numbers
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
        print(f"[WallpaperLoader] Directory does not exist: {dir}")
        return []

    wallpapers: List[Wallpaper] = []

    for wallpaper_folder in dir.iterdir():
        if not wallpaper_folder.is_dir():
            continue

        project_path = wallpaper_folder / "project.json"
        if not project_path.exists():
            print(
                f"[WallpaperLoader] Missing project.json in folder: {wallpaper_folder}"
            )
            continue

        try:
            with open(project_path, "r") as project_file:
                project = json.load(project_file)
        except json.JSONDecodeError as e:
            print(f"[WallpaperLoader] JSON parsing error in {project_path}: {e}")
            continue
        except Exception as e:
            print(
                f"[WallpaperLoader] Unexpected error reading {project_path}: {type(e).__name__}: {e}"
            )
            continue

        wallpaper = Wallpaper()

        contentrating = project.get("contentrating")
        if isinstance(contentrating, str):
            wallpaper.contentrating = contentrating
        elif contentrating is not None:
            print(
                f"[WallpaperLoader] Warning: contentrating has invalid type {type(contentrating).__name__} in {wallpaper_folder}"
            )

        file_name = project.get("file")
        if isinstance(file_name, str):
            wallpaper.file = wallpaper_folder / file_name
        elif file_name is not None:
            print(
                f"[WallpaperLoader] Warning: file has invalid type {type(file_name).__name__} in {wallpaper_folder}"
            )

        general = project.get("general")
        if isinstance(general, dict):
            properties_data = general.get("properties")
            if isinstance(properties_data, dict):
                properties: dict[str, WallpaperPropertyType] = {}

                for property_name, property_object in properties_data.items():
                    if not isinstance(property_object, dict):
                        print(
                            f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} is not a dictionary, skipping"
                        )
                        continue

                    prop_type = property_object.get("type")
                    prop_text = property_object.get("text")

                    if not isinstance(prop_type, str) or not isinstance(prop_text, str):
                        print(
                            f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} missing required fields 'type' or 'text', skipping"
                        )
                        continue

                    match prop_type:
                        case "bool":
                            prop_value = property_object.get("value")
                            if not isinstance(prop_value, bool):
                                print(
                                    f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} has invalid value type {type(prop_value).__name__} for bool, expected bool, skipping"
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
                                not isinstance(prop_min, numbers.Number)
                                or not isinstance(prop_max, numbers.Number)
                                or not isinstance(prop_value, numbers.Number)
                                or not isinstance(prop_editable, bool)
                            ):
                                invalid_fields = []
                                if not isinstance(prop_min, numbers.Number):
                                    invalid_fields.append(
                                        f"min ({type(prop_min).__name__})"
                                    )
                                if not isinstance(prop_max, numbers.Number):
                                    invalid_fields.append(
                                        f"max ({type(prop_max).__name__})"
                                    )
                                if not isinstance(prop_value, numbers.Number):
                                    invalid_fields.append(
                                        f"value ({type(prop_value).__name__})"
                                    )
                                if not isinstance(prop_editable, bool):
                                    invalid_fields.append(
                                        f"editable ({type(prop_editable).__name__})"
                                    )

                                print(
                                    f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} has invalid field types: {', '.join(invalid_fields)}, skipping"
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
                                print(
                                    f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} has invalid value type {type(prop_value).__name__} for color, expected str, skipping"
                                )
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
                                invalid_fields = []
                                if not isinstance(prop_options, list):
                                    invalid_fields.append(
                                        f"options ({type(prop_options).__name__})"
                                    )
                                if not isinstance(prop_value, int):
                                    invalid_fields.append(
                                        f"value ({type(prop_value).__name__})"
                                    )

                                print(
                                    f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} has invalid field types: {', '.join(invalid_fields)}, skipping"
                                )
                                continue

                            combo_options: List[ComboOptions] = []
                            for idx, option in enumerate(prop_options):
                                if not isinstance(option, dict):
                                    print(
                                        f"[WallpaperLoader] Warning: option {idx} in property '{property_name}' in {wallpaper_folder} is not a dictionary, skipping this option"
                                    )
                                    continue

                                option_label = option.get("label")
                                option_value = option.get("value")

                                if not isinstance(option_label, str) or not isinstance(
                                    option_value, int
                                ):
                                    invalid_option_fields = []
                                    if not isinstance(option_label, str):
                                        invalid_option_fields.append(
                                            f"label ({type(option_label).__name__})"
                                        )
                                    if not isinstance(option_value, int):
                                        invalid_option_fields.append(
                                            f"value ({type(option_value).__name__})"
                                        )

                                    print(
                                        f"[WallpaperLoader] Warning: option {idx} in property '{property_name}' in {wallpaper_folder} has invalid field types: {', '.join(invalid_option_fields)}, skipping this option"
                                    )
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
                                    f"[WallpaperLoader] Warning: property '{property_name}' in {wallpaper_folder} has invalid value type {type(prop_value).__name__} for textinput, expected str, skipping"
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
                                f"[WallpaperLoader] Warning: unsupported property type '{prop_type}' in property '{property_name}' in {wallpaper_folder}, skipping"
                            )
                            continue

                wallpaper.properties = properties
        elif general is not None:
            print(
                f"[WallpaperLoader] Warning: general has invalid type {type(general).__name__} in {wallpaper_folder}"
            )

        monetization = project.get("monetization")
        if isinstance(monetization, bool):
            wallpaper.monetization = monetization
        elif monetization is not None:
            print(
                f"[WallpaperLoader] Warning: monetization has invalid type {type(monetization).__name__} in {wallpaper_folder}"
            )

        preview_name = project.get("preview")
        if isinstance(preview_name, str):
            wallpaper.preview = wallpaper_folder / preview_name
        elif preview_name is not None:
            print(
                f"[WallpaperLoader] Warning: preview has invalid type {type(preview_name).__name__} in {wallpaper_folder}"
            )

        tags_data = project.get("tags")
        if isinstance(tags_data, list):
            tags: List[str] = []
            for idx, tag in enumerate(tags_data):
                if isinstance(tag, str):
                    tags.append(tag)
                else:
                    print(
                        f"[WallpaperLoader] Warning: tag at index {idx} in {wallpaper_folder} has invalid type {type(tag).__name__}, skipping this tag"
                    )
            wallpaper.tags = tags
        elif tags_data is not None:
            print(
                f"[WallpaperLoader] Warning: tags has invalid type {type(tags_data).__name__} in {wallpaper_folder}"
            )

        wallpaper_type = project.get("type")
        if not isinstance(wallpaper_type, str):
            print(
                f"[WallpaperLoader] Error: wallpaper in {wallpaper_folder} has invalid type field type {type(wallpaper_type).__name__}, expected str, skipping"
            )
            continue

        try:
            wallpaper.type = WallpaperType(wallpaper_type)
        except ValueError as e:
            print(
                f"[WallpaperLoader] Error: wallpaper in {wallpaper_folder} has invalid type value '{wallpaper_type}': {e}, skipping"
            )
            continue
        except Exception as e:
            print(
                f"[WallpaperLoader] Error: unexpected error processing wallpaper type in {wallpaper_folder}: {type(e).__name__}: {e}, skipping"
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
