from emoji import emojize
import os
from requests import get
from socket import gethostname, gethostbyname
import pickle
import platform
import sys
IN_COLAB = 'google.colab' in sys.modules

def check_notebook_name(expected_name):
    if not IN_COLAB:
        return None

    ip = gethostbyname(gethostname())  # 172.28.0.12
    notebook_name = get(f"http://{ip}:9000/api/sessions").json()[0]["name"]

    if notebook_name != expected_name:
        print(
            emojize(":warning:")
            + " このファイル名は `{}` でなければなりません。 / This should be named `{}`.".format(
                expected_name, expected_name
            )
        )
    else:
        print(
            emojize(":thumbs_up:")
            + " 正しいファイル名です。問題番号と対応しているか確認してください。 / The file name is correct. Please ensure it corresponds to the problem number."
        )


def do_objects_exist(names, notebook_globals):
    if IN_COLAB:
        print(
            emojize(":warning:")
            + " オブジェクトの存在確認のみ行っています。内容が正しいかどうかは確認していません。 / This only verifies the presence of the expected objects, without ensuring their contents are pertinent."
        )
        for name in names:
            if name in notebook_globals:
                print("  " + emojize(":thumbs_up:") + " object `{}` exists".format(name))
            else:
                print(
                    "  " + emojize(":construction:") + " object `{}` not found".format(name)
                )
    else:
        for name in names:
            if name in notebook_globals:
                with open(f'{name}.pickle', 'wb') as handle:
                    pickle.dump(notebook_globals[name], handle, protocol=pickle.HIGHEST_PROTOCOL)


def do_file_exists(names):
    print(
        emojize(":warning:")
        + " ファイルの存在確認のみ行っています。内容が正しいかどうかは確認していません / This solely confirms the existence of the expected files, without assuring the relevance of their contents."
    )
    for name in names:
        if os.path.exists(name):
            print("  " + emojize(":thumbs_up:") + " file `{}` exists".format(name))
        else:
            print(
                "  " + emojize(":construction:") + " file `{}` not found".format(name)
            )


def basic2(notebook_globals):
    check_notebook_name("basic2.ipynb")
    do_file_exists(
        [
            "/content/drive/MyDrive/ccp_ML/basic2.py",
            "/content/drive/MyDrive/ccp_ML/iris_X_0/statistics.csv",
        ]
    )


def basic3_1(notebook_globals):
    check_notebook_name("basic3-1.ipynb")
    do_objects_exist(
        [
            "scaler_X",
            "scaler_y",
            "X_train_scaled",
            "y_train_scaled",
            "X_test_scaled",
            "pls_model",
            "y_test_pred",
            "pls_model_grid",
            "y_test_pred_grid",
            "svr_model_grid",
            "y_test_pred_svr",
            "rf_model",
            "rf_model500",
            "y_test_pred_rf",
            "y_test_pred_rf500",
        ],
        notebook_globals,
    )
    do_file_exists(["SVR.png", "RF.png"])


def basic3_2(notebook_globals):
    check_notebook_name("basic3-2.ipynb")
    do_objects_exist(
        [
            "X_train",
            "X_test",
            "y_train",
            "y_test",
            "feature_names",
            "X_train_scaled",
            "y_train_scaled",
            "X_test_scaled",
            "models",
            "y_train_preds",
            "y_test_preds",
            "df",
            "importance_PLS",
            "importance_RF",
        ],
        notebook_globals,
    )

    do_file_exists(
        ["PLS.png", "SVR.png", "RF.png", "importance_PLS.png", "importance_RF.png"]
    )


def basic4_1(notebook_globals):
    check_notebook_name("basic4-1.ipynb")
    do_objects_exist(
        [
            "df",
            "X_train",
            "y_train",
            "x1",
            "x2",
            "X1",
            "X2",
            "X_test",
            "model_svm",
            "y_test_pred_svm",
            "model_rf",
            "y_test_pred_rf",
        ],
        notebook_globals,
    )
    do_file_exists(["SVC.png", "RandomForestClassifier.png"])


def basic4_2(notebook_globals):
    check_notebook_name("basic4-2.ipynb")
    do_objects_exist(
        [
            "iris",
            "X",
            "y",
            "feature_names",
            "target_names",
            "X_train",
            "X_test",
            "y_train",
            "y_test",
            "X_train_scaled",
            "X_test_scaled",
            "model_svm",
            "y_test_pred_svm",
            "matrix_svm",
            "model_rf",
            "y_test_pred_rf",
            "matrix_rf",
        ],
        notebook_globals,
    )
    # do_file_exists()


def app1(notebook_globals):
    check_notebook_name("app1.ipynb")
    do_objects_exist(
        [
            "X",
            "y",
            "df",
            "X_train",
            "X_test",
            "y_train",
            "y_test",
            "X_train_scaled",
            "y_train_scaled",
            "X_test_scaled",
            "df_metrics",
            "importance_PLS",
            "importance_RF",
        ],
        notebook_globals,
    )
    do_file_exists(
        ["PLS.png", "SVR.png", "RF.png", "importance_PLS.png", "importance_RF.png"]
    )


def app2(notebook_globals):
    check_notebook_name("app2.ipynb")
    do_objects_exist(
        [
            "move_vector_closer_to_largest_distribution",
            "plot_matrix_and_vector",
            "X",
            "p",
            "p0",
            "p1",
            "p2",
            "diff_t1",
            "diff_t2",
            "diff_t3",
            "t",
            "E",
            "myPCA",
            "model",
            "model_sk",
            "plot_class_components",
            "mean_X",
            "pc",
        ],
        notebook_globals,
    )


def app3(notebook_globals):
    check_notebook_name("app3.ipynb")
    do_file_exists(
        [
            "/content/drive/MyDrive/ccp_ML/mylib/regression/__init__.py",
            "/content/drive/MyDrive/ccp_ML/mylib/regression/GPDoE.py",
            "/content/drive/MyDrive/ccp_ML/mylib/__init__.py",
            "/content/drive/MyDrive/ccp_ML/test_GPDoE.py",
        ]
    )


def app4_1(notebook_globals):
    check_notebook_name("app4-1.ipynb")


def app4_2(notebook_globals):
    check_notebook_name("app4-2.ipynb")
    do_file_exists(["regression.csv", "classification.csv"])
