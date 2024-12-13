from app import create_app


import platform
import os
machine_processor = platform.processor()

the_java_home = "CONDA_PREFIX"
if "JAVA_HOME" in os.environ:
    the_java_home = "JAVA_HOME"

if machine_processor in ("x86_64", "x64"):
    machine_processor = "amd64"

# NOTE felipe try first with CONDA_PREFIX/jre/lib/amd64/server/libjvm.so
# (for older Java versions e.g. 8.x)
java_home_path = os.environ[the_java_home]
jvm_path = java_home_path

if not os.path.isfile(jvm_path):
    jvm_path = java_home_path + "/lib/" + machine_processor + "/server/libjvm.so"

if not os.path.isfile(jvm_path):
    # NOTE felipe try a second time using CONDA_PREFIX/lib/server/
    # (for newer java versions e.g. 11.x)
    jvm_path = os.environ[the_java_home] + "/lib/server/libjvm.so"
    if machine_processor == "amd64":
        if not os.path.isfile(jvm_path):
            jvm_path = (
                java_home_path + "/jre/lib/" + machine_processor + "/server/libjvm.so"
            )
    elif machine_processor in ("ppc64", "ppc64le"):
        jvm_path = (
            os.environ[the_java_home]
            + "/lib/"
            + machine_processor
            + "/default/libjvm.so"
        )
print("------------------------------")
print(the_java_home)
print(machine_processor)
print(jvm_path)
print("------------------------------")

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, port=8889, run_query_in_thread=True)
