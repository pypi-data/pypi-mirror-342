from .server import serve


def main():
    """MCP Maven Server - Maven command execute functionality for MCP"""
    import argparse
    import asyncio
    import json
    import os

    parser = argparse.ArgumentParser(
        description="give a model the ability to run maven command in a Java project."
    )
    parser.add_argument(
        "--java-home",
        type=str,
        default=None,
        help="Path to the Java home directory. If not specified, the system default will be used.",
    )
    parser.add_argument(
        "--mvn-executable",
        type=str,
        default=None,
        help="Path to the Maven executable. If not specified, the system default will be used.",
    )
    parser.add_argument(
        "--settings-file",
        type=str,
        default=None,
        help="Path to Maven settings file (e.g. ~/.m2/settings.xml).",
    )
    parser.add_argument(
        "--profiles",
        type=str,
        default=None,
        help="Comma-separated list of Maven profiles to activate or deactivate (prefix with ! to deactivate).",
    )
    parser.add_argument(
        "--system-properties",
        type=str,
        default=None,
        help='JSON format dictionary of system properties (e.g. \'{"maven.wagon.http.ssl.insecure": "true"}\').',
    )
    parser.add_argument(
        "--additional-args",
        type=str,
        default=None,
        help='JSON format list of additional Maven arguments (e.g. \'["-X", "-U"]\').',
    )
    parser.add_argument(
        "-o",
        "--offline",
        action="store_true",
        help="Run Maven in offline mode (no network access).",
    )
    # Last is the root directory
    parser.add_argument(
        "root_dir",
        type=str,
        default=".",
        help="Path to the root directory of the Maven project.",
    )

    args = parser.parse_args()

    # 处理配置文件参数
    profiles = args.profiles.split(",") if args.profiles else None

    # 处理系统属性和额外参数（从JSON格式解析）
    system_properties = None
    if args.system_properties:
        try:
            system_properties = json.loads(args.system_properties)
        except json.JSONDecodeError:
            print(
                f"Warning: Could not parse system properties JSON: {args.system_properties}"
            )
            print(
                'Format should be: \'{"property1": "value1", "property2": "value2"}\''
            )

    additional_args = None
    if args.additional_args:
        try:
            additional_args = json.loads(args.additional_args)
        except json.JSONDecodeError:
            print(
                f"Warning: Could not parse additional arguments JSON: {args.additional_args}"
            )
            print('Format should be: \'["-X", "-U"]\'')

    # 运行服务
    asyncio.run(
        serve(
            root_dir=args.root_dir,
            java_home=args.java_home,
            mvn_command=args.mvn_executable,
            settings_file=args.settings_file,
            profiles=profiles,
            system_properties=system_properties,
            additional_args=additional_args,
            offline=args.offline,
        )
    )


if __name__ == "__main__":
    main()
