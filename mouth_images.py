from PIL import Image


def getCelebImages(celeb, left=True):
    celeb_image_paths = {
        "Donald Trump": [
            "trump_closed_left.png",
            "trump_open_left.png",
            "trump_closed_right.png",
            "trump_open_right.png",
        ],
        "Taylor Swift": [
            "taylor_closed_left.png",
            "taylor_open_left.png",
            "taylor_closed_right.png",
            "taylor_open_right.png",
        ],
        "Kanye West": [
            "kanye_closed_left.png",
            "kanye_open_left.png",
            "kanye_closed_right.png",
            "kanye_open_right.png",
        ],
        "LeBron James": [
            "lebron_closed_left.png",
            "lebron_open_left.png",
            "lebron_closed_right.png",
            "lebron_open_right.png",
        ],
        "Morgan Freeman": [
            "freeman_closed_left.png",
            "freeman_open_left.png",
            "freeman_closed_right.png",
            "freeman_open_right.png",
        ],
        "Arnold Schwarzenegger": [
            "arnold_closed_left.png",
            "arnold_open_left.png",
            "arnold_closed_right.png",
            "arnold_open_right.png",
        ],
        "Peter Griffin": [
            "peter_closed_left.png",
            "peter_open_left.png",
            "peter_closed_right.png",
            "peter_open_right.png",
        ],
        "Lois Griffin": [
            "lois_closed_left.png",
            "lois_open_left.png",
            "lois_closed_right.png",
            "lois_open_right.png",
        ],
    }
    celeb_images = []
    if celeb not in celeb_image_paths.keys():
        return [
            Image.open("images/question_mark.png"),
            Image.open("images/question_mark.png"),
        ]
    for i in celeb_image_paths[celeb]:
        celeb_images.append(Image.open("images/" + i))
    if left:
        return celeb_images[2:4]
    return celeb_images[0:2]


def generatePodImages(podcast, celeb_images_left, celeb_images_right):
    pod_images = []
    for i in range(4):
        pod_images.append(podcast.copy())

    for i in range(2):
        for j in range(2):
            # print(pod_images[i * 2 + j])
            pod_images[i * 2 + j].paste(celeb_images_left[i], (281, 24, 431, 174))
            pod_images[i * 2 + j].paste(celeb_images_right[j], (1364, 24, 1514, 174))

    return pod_images


def getPodcastBackgrounds(celeb_left, celeb_right, path):
    podcast = Image.open("images/podcast_bg.png")
    left_celeb = getCelebImages(celeb_left, 1)
    right_celeb = getCelebImages(celeb_right, 0)
    pod_images = generatePodImages(podcast, left_celeb, right_celeb)
    print(path)

    pod_images[0].save(path + "no_talk.png")
    pod_images[1].save(path + "right_talk.png")
    pod_images[2].save(path + "left_talk.png")
    pod_images[3].save(path + "both_talk.png")


# getPodcastBackgrounds("Donald Trump", "Morgan Freeman", "pod_back/")


# Donald Trump
# Taylor Swift
# Kanye West
# Lebron James
