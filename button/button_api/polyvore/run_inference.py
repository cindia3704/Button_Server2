import tensorflow as tf
import pickle as pkl
import numpy as np
from . import configuration
from .import polyvore_model_bi as polyvore_model
import os
import json


def main():
    input1 = int(input("number 입력: "))
    sample_data = {"id": 22,
                   "clothID": 1000000,
                   "season": ["SPRING", "WINTER", "FALL"],
                   "category": "OUTER",
                   "photo": "17.jpg",
                   "style": ["SEMI-FORMAL", "CASUAL"],
                   "outfit": [6]
                   }
    extract_features(sample_data["id"], sample_data, input1)


def extract_features(id, serializer_data, number):
    for one_season in serializer_data["season"]:
        json_path = one_season + "_" + str(serializer_data["id"]) + ".json"

        if os.path.isfile(json_path):
            f = open(json_path, "r")
            json_dict = json.load(f)
            f.close()
            flag = False
            for one_item in json_dict[0]["items"]:
                if one_item["index"] == serializer_data["photo"].replace(".jpg", "").replace("/media/", ""):
                    flag = True
            if flag:
                continue
            else:
                json_dict[0]["items"].append({
                    "index": serializer_data["photo"].replace(".jpg", "").replace("/media/", "")
                })
                f2 = open(json_path, "w")
                json.dump(json_dict, f2)
                f2.close()
        else:
            output_data = []
            output_data.append(dict())
            output_data[0]["items"] = []
            output_data[0]["items"].append(dict())
            output_data[0]["items"][0]["index"] = serializer_data["photo"].replace(
                ".jpg", "").replace("/media/", "")
            output_data[0]["set_id"] = "media"
            f = open(json_path, "w")
            json.dump(output_data, f)
            f.close()

    g = tf.Graph()
    with g.as_default():
        model_config = configuration.ModelConfig()
        model_config.rnn_type = "lstm"
        model = polyvore_model.PolyvoreModel(model_config, mode="inference")
        model.build()
        saver = tf.train.Saver()

    g.finalize()
    sess = tf.Session(graph=g)
    # TODO :: 언니 여기 서버 모델있는 위치로 바꿔야해 ~
    saver.restore(sess, "button_api/model/model_final/model.ckpt-34865")

    for one_season in serializer_data["season"]:
        json_path = one_season + "_" + \
            str(serializer_data["id"]) + ".json"  # TODO :: change this path
        pkl_path = one_season + "_" + str(serializer_data["id"]) + ".pkl"

        test_json = json.load(open(json_path))
        test_features = dict()

        if number != 0:
            added_test_features = dict()
            for image_set in test_json:
                set_id = image_set["set_id"]
                image_feat = []
                image_rnn_feat = []
                ids = []
            for image in image_set["items"][number:]:
                filename = os.path.join("", set_id,
                                        # TODO K-jisoo u have to change this path to DJnago MEDIA dir
                                        str(image["index"]) + ".jpg")
                print(filename)
                with tf.gfile.GFile(filename, "r") as f:
                    image_feed = f.read()

                    [feat, rnn_feat] = sess.run([model.image_embeddings,
                                                 model.rnn_image_embeddings],
                                                feed_dict={"image_feed:0": image_feed})

                    image_name = set_id + "_" + str(image["index"])
                    added_test_features[image_name] = dict()
                    added_test_features[image_name]["image_feat"] = np.squeeze(
                        feat)
                    added_test_features[image_name]["image_rnn_feat"] = np.squeeze(
                        rnn_feat)

                    print(added_test_features)

            f = open(pkl_path, "rb")
            data = pkl.load(f)
            data.update(added_test_features)
            f.close()

            f = open(pkl_path, "wb")
            pkl.dump(data, f)
            f.close()
        if number == 0:
            # Save image ids and features in a dictionary.
            k = 0
            for image_set in test_json:
                set_id = image_set["set_id"]
                image_feat = []
                image_rnn_feat = []
                ids = []
                k = k + 1
                print(str(k) + " : " + set_id)
                for image in image_set["items"]:
                    filename = os.path.join("", set_id,
                                            str(image["index"]) + ".jpg")
                    with tf.gfile.GFile(filename, "r") as f:
                        image_feed = f.read()

                    [feat, rnn_feat] = sess.run([model.image_embeddings,
                                                 model.rnn_image_embeddings],
                                                feed_dict={"image_feed:0": image_feed})

                    image_name = set_id + "_" + str(image["index"])
                    test_features[image_name] = dict()
                    test_features[image_name]["image_feat"] = np.squeeze(feat)
                    test_features[image_name]["image_rnn_feat"] = np.squeeze(
                        rnn_feat)

                    # return input1

            with open(pkl_path, "wb") as f:
                print(number)
                pkl.dump(test_features, f)
                print(number)


if __name__ == "__main__":
    main()
