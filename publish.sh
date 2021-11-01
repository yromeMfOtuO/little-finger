# TIPS：setup.py 修改版本

function clean_build() {
    rm -rf ./dist/
    rm -rf ./build/
    rm -rf ./little_finger.egg-info/
}

# 清理构建目录
clean_build

# 构建
python3 setup.py sdist bdist_wheel

# 发布，需要输入用户名及密码
python3 -m twine upload dist/* -u <username> -p <password>
