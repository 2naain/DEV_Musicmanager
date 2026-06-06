from sqlmodel import Session, create_engine, select
from models.artist import ArtistID
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

descripciones = {
    1: (  # Kendrick Lamar
        "Rapero y compositor de Compton, California, considerado uno de los artistas más influyentes "
        "de su generación. Ganador del Premio Pulitzer de Música en 2018, el primero otorgado a un "
        "artista no clásico ni de jazz. Sus álbumes más aclamados incluyen 'good kid, m.A.A.d city' "
        "(2012), 'To Pimp a Butterfly' (2015) y 'DAMN.' (2017), este último ganador del Grammy al "
        "Mejor Álbum de Rap. En 2023 lanzó 'Mr. Morale & The Big Steppers', otro éxito crítico."
    ),
    2: (  # Mac Miller
        "Rapero y productor de Pittsburgh, Pennsylvania, conocido por su evolución artística desde "
        "el hip-hop optimista hasta exploraciones profundas del jazz, el soul y la psicodelia. "
        "Sus álbumes más queridos incluyen 'Blue Slide Park' (2011), 'Watching Movies with the Sound "
        "Off' (2013), 'The Divine Feminine' (2016) y 'Swimming' (2018). Falleció en septiembre de "
        "2018, dejando un legado enorme. Su álbum póstumo 'Circles' (2020) fue recibido con gran emotividad."
    ),
    3: (  # Bad Bunny
        "Cantante y compositor puertorriqueño nacido como Benito Antonio Martínez Ocasio, máximo "
        "exponente del reggaetón y trap latino a nivel mundial. Ha sido el artista más escuchado en "
        "Spotify durante varios años consecutivos. Entre sus álbumes más exitosos destacan 'X 100PRE' "
        "(2018), 'YHLQMDLG' (2020), 'El Último Tour Del Mundo' (2020) y 'Un Verano Sin Ti' (2022), "
        "primer álbum en español en encabezar el Billboard 200."
    ),
    4: (  # John Coltrane
        "Saxofonista y compositor estadounidense, figura central del jazz moderno del siglo XX. "
        "Revolucionó el género con su técnica del 'sheets of sound' y sus exploraciones del jazz modal "
        "y espiritual. Sus obras maestras incluyen 'Giant Steps' (1960), 'My Favorite Things' (1961), "
        "'A Love Supreme' (1965) —considerado uno de los mejores álbumes de la historia— y "
        "'Ascension' (1966). Fue incluido póstumamente en el Salón de la Fama del Grammy."
    ),
    5: (  # Michael Jackson
        "Conocido como el Rey del Pop, Michael Jackson es el artista musical más exitoso de todos los "
        "tiempos. Con inicio en The Jackson 5, su carrera en solitario redefinió la música popular, "
        "el videoclip y el espectáculo en vivo. Sus álbumes 'Off the Wall' (1979), 'Thriller' (1982) "
        "—el más vendido de la historia con más de 70 millones de copias— 'Bad' (1987) y 'Dangerous' "
        "(1991) son hitos de la cultura global. Ganó 13 premios Grammy a lo largo de su carrera."
    ),
    6: (  # Guns N Roses
        "Banda de hard rock formada en Los Ángeles en 1985, liderada por el vocalista Axl Rose y el "
        "guitarrista Slash. Uno de los grupos más vendidos de la historia con más de 100 millones de "
        "álbumes vendidos. Su debut 'Appetite for Destruction' (1987) es el álbum debut más vendido "
        "en EE.UU., con canciones icónicas como 'Welcome to the Jungle' y 'Sweet Child O' Mine'. "
        "Otros álbumes destacados son 'Use Your Illusion I y II' (1991) y 'Chinese Democracy' (2008)."
    ),
    7: (  # Daft Punk
        "Dúo francés de música electrónica formado por Thomas Bangalter y Guy-Manuel de Homem-Christo, "
        "considerados los artistas más influyentes de la música electrónica moderna. Conocidos por sus "
        "icónicos cascos de robot, transformaron el house y el techno en fenómenos globales. Sus álbumes "
        "'Homework' (1997), 'Discovery' (2001) y 'Random Access Memories' (2013) son referencias del "
        "género. Este último ganó el Grammy al Álbum del Año. Se separaron en 2021."
    ),
    8: (  # Beethoven
        "Ludwig van Beethoven fue un compositor y pianista alemán (1770-1827), considerado uno de los "
        "más grandes compositores de la historia de la música occidental. Compuso durante la transición "
        "entre el Clasicismo y el Romanticismo. Obras maestras como la Sinfonía N.º 5, la Sinfonía N.º 9 "
        "(compuesta cuando ya era completamente sordo), la Sonata 'Claro de Luna' y el Concierto para "
        "piano N.º 5 'Emperador' siguen siendo referentes universales más de 200 años después de su creación."
    ),
    9: (  # Arctic Monkeys
        "Banda de rock originaria de Sheffield, Inglaterra, formada en 2002. Uno de los grupos británicos "
        "más exitosos del siglo XXI, conocidos por sus letras agudas y su sonido que va del indie rock "
        "al garage rock y el rock psicodélico. Su debut 'Whatever People Say I Am, That's What I'm Not' "
        "(2006) fue el álbum debut más vendido en la historia del Reino Unido. Otros álbumes icónicos "
        "incluyen 'AM' (2013) y 'Tranquility Base Hotel + Casino' (2018)."
    ),
    10: (  # XXXTENTACION
        "Rapero y cantante de Florida, nacido como Jahseh Dwayne Ricardo Onfroy, conocido por su estilo "
        "ecléctico que mezclaba trap, emo rap, rock y R&B. A pesar de su corta carrera y vida, dejó una "
        "huella profunda en la cultura del rap alternativo. Sus álbumes '17' (2017) y '?' (2018) exploraron "
        "temas de depresión, amor y violencia con una crudeza poco común. Falleció en junio de 2018 a los "
        "20 años. Su música sigue siendo ampliamente escuchada por las nuevas generaciones."
    ),
}

with Session(engine) as session:
    for artist_id, descripcion in descripciones.items():
        artist = session.get(ArtistID, artist_id)
        if artist:
            artist.descripcion = descripcion
            session.add(artist)
            print(f"✓ {artist.name}")
        else:
            print(f"✗ ID {artist_id} no encontrado")
    session.commit()
    print("\nDone — descripciones actualizadas.")