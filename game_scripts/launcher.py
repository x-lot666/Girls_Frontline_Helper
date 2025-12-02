import yaml
import importlib

BASE_PATH = "game_scripts.battle"


def run_task(task):
    mtype = task["type"]  # 脚本文件夹(main_mission / event_mission)
    level = task["level"]  # 脚本名称(a_normal / shattered_connexion_running / ...)
    args = task.get("args", [])

    module_path = f"{BASE_PATH}.{mtype}.{level}"
    module = importlib.import_module(module_path)

    module.main(*args)


def main():
    tasks = yaml.safe_load(open("mission_plan.yaml", encoding="utf8"))

    for t in tasks:
        run_task(t)


if __name__ == "__main__":
    main()
