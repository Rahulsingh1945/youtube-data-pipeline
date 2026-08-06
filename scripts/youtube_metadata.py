from yt_dlp import YoutubeDL
import pandas as pd
from pathlib import Path


# ============================================
# Add YouTube channel URLs here
# ============================================

channels = [

    # Programming / Software
    "https://www.youtube.com/@freecodecamp",
    "https://www.youtube.com/@Fireship",
    "https://www.youtube.com/@TraversyMedia",
    "https://www.youtube.com/@ProgrammingwithMosh",
    "https://www.youtube.com/@Coreyms",

    # Data Science / AI
    "https://www.youtube.com/@3blue1brown",
    "https://www.youtube.com/@sentdex",
    "https://www.youtube.com/@StatQuest",
    "https://www.youtube.com/@KrishNaik",
    "https://www.youtube.com/@AlexTheAnalyst",

    # Science / Education
    "https://www.youtube.com/@Veritasium",
    "https://www.youtube.com/@kurzgesagt",
    "https://www.youtube.com/@smartereveryday",
    "https://www.youtube.com/@numberphile",
    "https://www.youtube.com/@Vsauce",

    # Technology
    "https://www.youtube.com/@LinusTechTips",
    "https://www.youtube.com/@mkbhd",
    "https://www.youtube.com/@TheEngineeringMindset",

    # Business
    "https://www.youtube.com/@AliAbdaal",
    "https://www.youtube.com/@YCombinator"

]


# ============================================
# Output location
# ============================================

project_root = Path(__file__).resolve().parent.parent

output = (
    project_root
    / "data"
    / "raw"
    / "youtube_dataset.csv"
)

output.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================
# Load existing data
# ============================================

if output.exists():

    old_df = pd.read_csv(output)

    all_data = old_df.to_dict(
        "records"
    )

    existing_ids = set(
        old_df["video_id"].astype(str)
    )

    print(
        f"Existing videos: {len(existing_ids)}"
    )

else:

    all_data = []

    existing_ids = set()

    print(
        "Starting new dataset"
    )



# ============================================
# yt-dlp options
# ============================================

playlist_opts = {

    "quiet": True,
    "extract_flat": True,
    "skip_download": True

}


video_opts = {

    "quiet": True,
    "skip_download": True

}



# ============================================
# Channel loop
# ============================================

for channel_no, channel_url in enumerate(channels, start=1):

    print("\n" + "=" * 60)
    print(
        f"CHANNEL {channel_no}: {channel_url}"
    )
    print("=" * 60)


    try:

        playlists_url = (
            channel_url.rstrip("/")
            + "/playlists"
        )


        with YoutubeDL(playlist_opts) as ydl:

            channel_info = ydl.extract_info(
                playlists_url,
                download=False
            )


        playlists = channel_info.get(
            "entries",
            []
        )


        print(
            f"Playlists found: {len(playlists)}"
        )



        # ====================================
        # Playlist loop
        # ====================================

        for playlist in playlists:


            playlist_id = playlist.get(
                "id"
            )


            playlist_url = (
                "https://www.youtube.com/playlist?list="
                + playlist_id
            )


            playlist_title = playlist.get(
                "title",
                "Unknown Playlist"
            )


            print(
                f"\nPlaylist: {playlist_title}"
            )


            try:

                with YoutubeDL(playlist_opts) as ydl:

                    playlist_data = ydl.extract_info(
                        playlist_url,
                        download=False
                    )


                videos = playlist_data.get(
                    "entries",
                    []
                )


                print(
                    f"Videos found: {len(videos)}"
                )


                # ====================================
                # Video loop
                # ====================================

                for i, video in enumerate(videos, start=1):


                    video_id = str(
                        video.get("id")
                    )


                    # Skip already collected videos

                    if video_id in existing_ids:

                        print(
                            "Already exists:",
                            video_id
                        )

                        continue



                    video_url = (
                        "https://www.youtube.com/watch?v="
                        + video_id
                    )


                    print(
                        f"[{i}/{len(videos)}]"
                    )



                    try:

                        with YoutubeDL(video_opts) as ydl:

                            data = ydl.extract_info(
                                video_url,
                                download=False
                            )


                        row = {


                            "channel_source": channel_url,

                            "playlist": playlist_title,

                            "video_id": data.get("id"),

                            "title": data.get("title"),

                            "channel": data.get("uploader"),

                            "upload_date": data.get("upload_date"),

                            "duration": data.get("duration"),

                            "views": data.get("view_count"),

                            "likes": data.get("like_count"),

                            "comments": data.get("comment_count"),

                            "tags": ", ".join(
                                data.get("tags", [])
                            ),

                            "category": ", ".join(
                                data.get("categories", [])
                            )

                        }



                        all_data.append(row)

                        existing_ids.add(video_id)



                        # Save checkpoint

                        if len(all_data) % 50 == 0:


                            df = pd.DataFrame(
                                all_data
                            )


                            df.to_csv(
                                output,
                                index=False
                            )


                            print(
                                f"Checkpoint saved: {len(df)} videos"
                            )



                    except Exception as e:

                        print(
                            "Video skipped:",
                            e
                        )


            except Exception as e:

                print(
                    "Playlist error:",
                    e
                )


    except Exception as e:

        print(
            "Channel error:",
            e
        )



# ============================================
# Final save
# ============================================

df = pd.DataFrame(
    all_data
)


df.to_csv(
    output,
    index=False
)


print("\n" + "=" * 60)
print("FINISHED")
print("=" * 60)

print(
    f"Total videos collected: {len(df)}"
)

print(
    f"Saved at: {output}"
)