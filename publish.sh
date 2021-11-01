# TIPS：setup.py 修改版本

function clean() {
    rm -rf ./dist/
    rm -rf ./build/
    rm -rf ./little_finger.egg-info/
    echo 'clean Successfully'
}

function build() {
    echo 'build start ...'
    # 构建
    python3 setup.py sdist bdist_wheel
    echo 'build Successfully'
}

function upload() {
    echo 'upload start'
    # 发布，需要输入用户名及密码
    python3 -m twine upload dist/* -u '<username>' -p '<password>'
    echo 'upload Successfully'
}

# 清理构建目录
echo 'clean before build ...'
clean
build
upload
# 重新清理构建目录
echo 'clean after upload ...'
clean
