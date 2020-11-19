import mini.pkg_tool as Tool

robot_id = "0090"

if __name__ == '__main__':
    # Query alphamini package information
    # info = Tool.query_py_pkg(pkg_name="alphamini", robot_id=robot_id)
    # print(f'{info}')
    #
    # # List py packages in the robot
    # list_info = Tool.list_py_pkg(robot_id=robot_id)
    # print(f'{list_info}')
    #
    # # Install the simple_socket-0.0.2-py3-none-any.whl file in the current directory
    # Tool.install_py_pkg(package_path="simple_socket-0.0.2-py3-none-any.whl", robot_id=robot_id, debug=True)
    # # Uninstall simple_socket
    # Tool.uninstall_py_pkg(pkg_name="simple-socket", robot_id=robot_id, debug=True)

    # Package the tts_demo project in the current directory into py wheel, and the return value is the wheel path after packaged generation
    pkg_path = Tool.setup_py_pkg("tts_demo")
    print(f'{pkg_path}')

    # Uninstall tts_demo
    Tool.uninstall_py_pkg(pkg_name="tts_demo", robot_id=robot_id)

    # Reinstall the packaged tts_demo
    Tool.install_py_pkg(package_path=pkg_path, robot_id=robot_id, debug=False)

    # Trigger tts_demo offline execution
    Tool.run_py_pkg("tts_demo", robot_id=robot_id)
