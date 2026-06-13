<div align="center">

# 🖼️ linux-wallpaperengine-gui

**Минималистичный GUI-клиент для [linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine/)**

![GitHub License](https://img.shields.io/github/license/Dimidroll06/linux-wallpaperengine-gui?style=for-the-badge&color=blue)
![Python Version](https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Status](https://img.shields.io/badge/status-archived%20%2F%20unfinished-orange?style=for-the-badge)
![Wayland](https://img.shields.io/badge/Wayland-Hyprland%20%7C%20Sway-blueviolet?style=for-the-badge)

<br>

<img src="./public/img1.png" alt="linux-wallpaperengine-gui Screenshot" width="800" style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);">

</div>

---

## 📖 О проекте

`linux-wallpaperengine-gui` — это максимально простой и ненавязчивый графический интерфейс для управления живыми обоями через библиотеку `linux-wallpaperengine`. 

Приложение спроектировано так, чтобы **не мешать пользователю**: оно запускается напрямую в системный трей, автоматически подгружая последние использованные обои. Главное окно открывается только по запросу (через контекстное меню трея -> *Show Window*).

---

## ⚠️ Важное уведомление (Текущий статус)

> **🚧 Проект временно архивирован и является недописанным.**
> 
> Это связано с тем, что базовая библиотека (`linux-wallpaperengine`), на которой он построен, также находится в стадии активной разработки и имеет ряд критических недоработок:
> - **Ошибки FFmpeg:** Наблюдаются явные проблемы при загрузке и рендере обоев типа `VIDEO`.
> - **Неполная поддержка SCENE:** Обои типа `SCENE` (сцены) работают некорректно или не поддерживают часть функций.
> 
> Из-за этих ограничений на стороне бэкенда, реализовать задуманный функционал в полном объеме сейчас невозможно. 
> 
> **Планы на будущее:** Как только библиотека будет дописана или вышеуказанные ошибки будут исправлены, проект будет разморожен. В планах: добавление поддержки скриптинга, интеграция с `pywal` для автоматической смены тем и общая полировка интерфейса.

---

## 🚀 Запуск и Использование

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Dimidroll06/linux-wallpaperengine-gui.git
   cd linux-wallpaperengine-gui
   ```
2. Установите зависимости (рекомендуется использовать виртуальное окружение):
   ```bash
   pip install -r requirements.txt
   ```

### Запуск
Главный файл запуска — `main.py`:
```bash
python main.py
```
После запуска иконка появится в системном трее. Нажмите на неё правой кнопкой мыши и выберите **Show Window**, чтобы открыть настройки.

### 🔄 Автозагрузка (Рекомендуется)
Так как приложение должно предварительно загружать обои в фоне, его **крайне рекомендуется добавлять в автозагрузку** вашего оконного менеджера или окружения рабочего стола.

**Для Hyprland:**
Добавьте в `~/.config/hypr/hyprland.conf`:
```ini
exec-once = /путь/до/venv/bin/python /путь/до/linux-wallpaperengine-gui/main.py
```

**Для Sway:**
Добавьте в `~/.config/sway/config`:
```text
exec /путь/до/venv/bin/python /путь/до/linux-wallpaperengine-gui/main.py
```

**Для GNOME / KDE / XFCE:**
Добавьте команду `python /путь/до/main.py` в раздел "Автозапуск приложений" (Autostart) в настройках вашей среды.

---

## 📂 Структура проекта

```text
├── LICENSE                 # Лицензия GPL-3.0
├── main.py                 # Точка входа в приложение
├── pyrightconfig.json      # Конфигурация статического анализатора типов
├── README-RU.md            # Этот файл
├── requirements.txt        # Зависимости Python
└── src
    ├── config.py           # Глобальные конфигурации и пути
    ├── controllers/        # Контроллеры (связь между UI и логикой)
    ├── core/               # Ядро приложения
    │   ├── lib.py          # Обертка над linux-wallpaperengine
    │   └── state_manager.py# Управление состоянием (сохранение/загрузка)
    ├── gui/                # Графический интерфейс (PyQt6)
    │   ├── application.py  # Инициализация QApplication
    │   ├── main_window.py  # Главное окно настроек
    │   ├── tray.py         # Логика системного трея
    │   ├── resources/      # Ресурсы (иконки, стили)
    │   │   ├── icon512.png
    │   │   ├── icon.png
    │   │   └── style.qss   # Таблица стилей Qt
    │   └── widgets/        # Кастомные виджеты
    │       └── wallpaper_grid.py # Сетка превью обоев
    ├── models/             # Модели данных (Pydantic/Dataclasses)
    │   └── wallpaper.py    # Описание структур обоев и их свойств
    └── utils/              # Вспомогательные утилиты
        ├── singleton.py    # Паттерн Singleton
        └── wallpaper_loader.py # Загрузчик метаданных обоев
```

---

## 🗺️ Roadmap (Планы после разморозки)

- [ ] **Скриптинг:** Поддержка выполнения пользовательских скриптов внутри обоев типа SCENE.
- [ ] **Интеграция с Pywal:** Автоматическое извлечение цветовой палитры из текущих обоев и применение её ко всей системе.
- [ ] **Исправление VIDEO:** Полная поддержка видео-обоев после фикса багов FFmpeg в upstream-библиотеке.
- [ ] **UI/UX:** Улучшение сетки превью, добавление прогресс-баров загрузки и более гибкая настройка свойств (слайдеры, цвета).

---

## ⚖️ Лицензия

Этот проект распространяется под лицензией **GNU General Public License v3.0 (GPL-3.0)**. 
Выбор данной лицензии обусловлен тем, что проект является надстройкой над библиотекой `linux-wallpaperengine`, которая также распространяется под GPL-3.0.

Подробнее см. файл [LICENSE](./LICENSE).
