import mini.pkg_tool as Tool

robot_id = "0090"

if __name__ == '__main__':
    # 查询alphamini包信息
    # info = Tool.query_py_pkg(pkg_name="alphamini", robot_id=robot_id)
    # print(f'{info}')
    #
    # # 列出机器人内py包
    # list_info = Tool.list_py_pkg(robot_id=robot_id)
    # print(f'{list_info}')
    #
    # # 安装当前目录下simple_socket-0.0.2-py3-none-any.whl文件
    # Tool.install_py_pkg(package_path="simple_socket-0.0.2-py3-none-any.whl", robot_id=robot_id, debug=True)
    # # 卸载simple_socket
    # Tool.uninstall_py_pkg(pkg_name="simple-socket", robot_id=robot_id, debug=True)

    # 将当前目录下的tts_demo工程打包成py wheel， 返回值为打包生成后的wheel路径
    pkg_path = Tool.setup_py_pkg("tts_demo")
    print(f'{pkg_path}')

    # 卸载tts_demo
    Tool.uninstall_py_pkg(pkg_name="tts_demo", robot_id=robot_id)

    # 重新安装打包后的tts_demo
    Tool.install_py_pkg(package_path=pkg_path, robot_id=robot_id, debug=False)

    # 触发tts_demo脱机执行
    Tool.run_py_pkg("tts_demo", robot_id=robot_id)
