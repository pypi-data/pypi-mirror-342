from pymusement.parks.universal.UniversalStudiosFlorida import UniversalStudiosFlorida
from pymusement.parks.universal.IslandsOfAdventure import IslandsOfAdventure
from pymusement.parks.universal.UniversalHollywood import UniversalHollywood
from pymusement.parks.universal.UniversalVolcano import UniversalVolcano
from pymusement.parks.universal.UniversalEpicUniverse import UniversalEpicUniverse
from pymusement.parks.HersheyPark import HersheyPark
from pymusement.parks.disney.AnimalKingdom import AnimalKingdom
from pymusement.parks.disney.CaliforniaAdventure import CaliforniaAdventure
from pymusement.parks.disney.Disneyland import Disneyland
from pymusement.parks.disney.Epcot import Epcot
from pymusement.parks.disney.HollywoodStudios import HollywoodStudios
from pymusement.parks.disney.MagicKingdom import MagicKingdom
from pymusement.parks.sixflags.SixFlagsOverTexas import SixFlagsOverTexas
from pymusement.parks.sixflags.SixFlagsOverGeorgia import SixFlagsOverGeorgia
from pymusement.parks.sixflags.SixFlagsStLouis import SixFlagsStLouis
from pymusement.parks.sixflags.SixFlagsGreatAdventure import SixFlagsGreatAdventure
from pymusement.parks.sixflags.SixFlagsMagicMountain import SixFlagsMagicMountain
from pymusement.parks.sixflags.SixFlagsGreatAmerica import SixFlagsGreatAmerica
from pymusement.parks.sixflags.SixFlagsFiestaTexas import SixFlagsFiestaTexas
from pymusement.parks.sixflags.SixFlagsHurricaneHarborArlington import SixFlagsHurricaneHarborArlington
from pymusement.parks.sixflags.SixFlagsHurricaneHarborLosAngeles import SixFlagsHurricaneHarborLosAngeles
from pymusement.parks.sixflags.SixFlagsHurricaneHarborChicago import SixFlagsHurricaneHarborChicago
from pymusement.parks.sixflags.SixFlagsAmerica import SixFlagsAmerica
from pymusement.parks.sixflags.SixFlagsDiscoveryKingdom import SixFlagsDiscoveryKingdom
from pymusement.parks.sixflags.SixFlagsNewEngland import SixFlagsNewEngland
from pymusement.parks.sixflags.SixFlagsHurricaneHarborJackson import SixFlagsHurricaneHarborJackson
from pymusement.parks.sixflags.TheGreatEscape import TheGreatEscape
from pymusement.parks.sixflags.SixFlagsWhiteWaterAtlanta import SixFlagsWhiteWaterAtlanta
from pymusement.parks.sixflags.SixFlagsMexico import SixFlagsMexico
from pymusement.parks.sixflags.LaRondeMontreal import LaRondeMontreal
from pymusement.parks.sixflags.SixFlagsHurricaneHarborOaxtepec import SixFlagsHurricaneHarborOaxtepec
from pymusement.parks.sixflags.SixFlagsHurricaneHarborConcord import SixFlagsHurricaneHarborConcord
from pymusement.parks.sixflags.SixFlagsFrontierCity import SixFlagsFrontierCity
from pymusement.parks.sixflags.SixFlagsHurricaneHarborOklahomaCity import SixFlagsHurricaneHarborOklahomaCity
from pymusement.parks.sixflags.SixFlagsDarienLake import SixFlagsDarienLake
from pymusement.parks.sixflags.SixFlagsHurricaneHarborPhoenix import SixFlagsHurricaneHarborPhoenix
from pymusement.parks.sixflags.SixFlagsHurricaneHarborSplashTown import SixFlagsHurricaneHarborSplashTown
from pymusement.parks.sixflags.SixFlagsHurricaneHarborRockford import SixFlagsHurricaneHarborRockford
from pymusement.parks.seaworld.SeaworldOrlando import SeaworldOrlando
from pymusement.parks.seaworld.BuschGardensTampa import BuschGardensTampa
from pymusement.parks.seaworld.SeaworldSanAntonio import SeaworldSanAntonio
from pymusement.parks.seaworld.SeaworldSanDiego import SeaworldSanDiego
from pymusement.parks.seaworld.BuschGardensWilliamsburg import BuschGardensWilliamsburg



PARKS = {
    'universal-florida' : UniversalStudiosFlorida(),
    'islands-adventure' : IslandsOfAdventure(),
    'universal-hollywood' : UniversalHollywood(),
    'volcano-bay' : UniversalVolcano(),
    'epic-universe' : UniversalEpicUniverse(),
    'hersheypark' : HersheyPark(),
    'magic-kingdom' : MagicKingdom(),
    'animal-kingdom' : AnimalKingdom(),
    'epcot' : Epcot(),
    'hollywood-studios':HollywoodStudios(),
    'disneyland': Disneyland(),
    'california-adventure' : CaliforniaAdventure(),
    'six-flags-over-texas' : SixFlagsOverTexas(),
	'six-flags-over-georgia' : SixFlagsOverGeorgia(),
	'six-flags-st-louis' : SixFlagsStLouis(),
	'six-flags-great-adventure' : SixFlagsGreatAdventure(),
	'six-flags-magic-mountain' : SixFlagsMagicMountain(),
	'six-flags-great-america' : SixFlagsGreatAmerica(),
	'six-flags-fiesta-texas' : SixFlagsFiestaTexas(),
	'six-flags-hurricane-harbor-arlington' : SixFlagsHurricaneHarborArlington(),
	'six-flags-hurricane-harbor-los-angeles' : SixFlagsHurricaneHarborLosAngeles(),
	'six-flags-hurricane-harbor-chicago' : SixFlagsHurricaneHarborChicago(),
	'six-flags-america' : SixFlagsAmerica(),
	'six-flags-discovery-kingdom' : SixFlagsDiscoveryKingdom(),
	'six-flags-new-england' : SixFlagsNewEngland(),
	'six-flags-hurricane-harbor-jackson' : SixFlagsHurricaneHarborJackson(),
	'the-great-escape' : TheGreatEscape(),
	'six-flags-white-water-atlanta' : SixFlagsWhiteWaterAtlanta(),
	'six-flags-mexico' : SixFlagsMexico(),
	'la-ronde-montreal' : LaRondeMontreal(),
	'six-flags-hurricane-harbor-oaxtepec' : SixFlagsHurricaneHarborOaxtepec(),
	'six-flags-hurricane-harbor-concord' : SixFlagsHurricaneHarborConcord(),
	'six-flags-frontier-city' : SixFlagsFrontierCity(),
	'six-flags-hurricane-harbor-oklahoma-city' : SixFlagsHurricaneHarborOklahomaCity(),
	'six-flags-darien-lake' : SixFlagsDarienLake(),
	'six-flags-hurricane-harbor-phoenix' : SixFlagsHurricaneHarborPhoenix(),
	'six-flags-hurricane-harbor-splashtown' : SixFlagsHurricaneHarborSplashTown(),
	'six-flags-hurricane-harbor-rockford' : SixFlagsHurricaneHarborRockford(),
	'seaworld-orlando' : SeaworldOrlando(),
    'busch-gardens-tampa' : BuschGardensTampa(),
    'seaworld-san-antonio' : SeaworldSanAntonio(),
    'seaworld-san-diego' : SeaworldSanDiego(),
    'busch-gardens-williamsburg' : BuschGardensWilliamsburg()
}
