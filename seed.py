from sqlmodel import Session
from db import engine
from models.artist import ArtistBase
from models.song import SongBase
from models.playlist import PlaylistBase
from operations.operations_artist_db import createArtist
from operations.operations_song_db import createSong_db
from operations.operations_playlist_db import create_playlist, add_song_to_playlist
import asyncio


async def seed():
    with Session(engine) as session:
        # Artistas
        kendrick = createArtist(ArtistBase(name="Kendrick Lamar"), session)
        mac = createArtist(ArtistBase(name="Mac Miller"), session)
        bad_bunny = createArtist(ArtistBase(name="Bad Bunny"), session)
        coltrane = createArtist(ArtistBase(name="John Coltrane"), session)
        michael = createArtist(ArtistBase(name="Michael Jackson"), session)
        gnr = createArtist(ArtistBase(name="Guns N Roses"), session)
        daft_punk = createArtist(ArtistBase(name="Daft Punk"), session)
        beethoven = createArtist(ArtistBase(name="Beethoven"), session)
        arctic = createArtist(ArtistBase(name="Arctic Monkeys"), session)

        s1 = await createSong_db(
            SongBase(title="Sing About Me Im Dying of Thirst", genre="hiphop", duration=724, artist_id=kendrick.id),
            session)
        s2 = await createSong_db(SongBase(title="Real", genre="hiphop", duration=443, artist_id=kendrick.id), session)
        s3 = await createSong_db(SongBase(title="Cinderella", genre="hiphop", duration=480, artist_id=mac.id), session)
        s4 = await createSong_db(SongBase(title="ROS", genre="hiphop", duration=343, artist_id=mac.id), session)
        s5 = await createSong_db(
            SongBase(title="Titi Me Pregunto", genre="reggaeton", duration=197, artist_id=bad_bunny.id), session)
        s6 = await createSong_db(SongBase(title="Efecto", genre="reggaeton", duration=178, artist_id=bad_bunny.id),
                                 session)
        s7 = await createSong_db(SongBase(title="A Love Supreme", genre="jazz", duration=520, artist_id=coltrane.id),
                                 session)
        s8 = await createSong_db(
            SongBase(title="My Favorite Things", genre="jazz", duration=435, artist_id=coltrane.id), session)
        s9 = await createSong_db(SongBase(title="Billie Jean", genre="pop", duration=297, artist_id=michael.id),
                                 session)
        s10 = await createSong_db(SongBase(title="Thriller", genre="pop", duration=358, artist_id=michael.id), session)
        s11 = await createSong_db(SongBase(title="November Rain", genre="rock", duration=537, artist_id=gnr.id),
                                  session)
        s12 = await createSong_db(SongBase(title="Sweet Child O Mine", genre="rock", duration=355, artist_id=gnr.id),
                                  session)
        s13 = await createSong_db(
            SongBase(title="Get Lucky", genre="electronica", duration=248, artist_id=daft_punk.id), session)
        s14 = await createSong_db(
            SongBase(title="Harder Better Faster", genre="electronica", duration=224, artist_id=daft_punk.id), session)
        s15 = await createSong_db(
            SongBase(title="Moonlight Sonata", genre="clasica", duration=900, artist_id=beethoven.id), session)
        s16 = await createSong_db(
            SongBase(title="Symphony No. 5", genre="clasica", duration=1980, artist_id=beethoven.id), session)
        s17 = await createSong_db(SongBase(title="R U Mine?", genre="metal", duration=201, artist_id=arctic.id),
                                  session)
        s18 = await createSong_db(SongBase(title="Do I Wanna Know?", genre="metal", duration=272, artist_id=arctic.id),
session)

        # Playlists
        p1 = create_playlist(PlaylistBase(name="Music Itself", description="Las canciones que hablan por si solas"), session)
        p2 = create_playlist(PlaylistBase(name="Chill vibes", description="Para relajarse"), session)
        p3 = create_playlist(PlaylistBase(name="Clasicos de siempre", description="Lo mejor de todos los generos"), session)

        # Canciones en playlists
        add_song_to_playlist(p1.id, s2.id, session)
        add_song_to_playlist(p1.id, s11.id, session)
        add_song_to_playlist(p1.id, s12.id, session)
        add_song_to_playlist(p1.id, s17.id, session)

        add_song_to_playlist(p2.id, s1.id, session)
        add_song_to_playlist(p2.id, s3.id, session)
        add_song_to_playlist(p2.id, s7.id, session)
        add_song_to_playlist(p2.id, s15.id, session)

        add_song_to_playlist(p3.id, s5.id, session)
        add_song_to_playlist(p3.id, s9.id, session)
        add_song_to_playlist(p3.id, s13.id, session)
        add_song_to_playlist(p3.id, s18.id, session)

        print("Seed completado")


asyncio.run(seed())