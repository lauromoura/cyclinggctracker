module Models exposing (..)

import RemoteData exposing (WebData)


type alias Model =
    { riders : WebData (List Rider)
    , count : Int
    }


type alias Rider =
    { name : String
    , info : RiderInfo
    }


type alias RiderInfo =
    { position : Position
    , times : List Int
    , team : String
    }


initialModel : Model
initialModel =
    { riders = RemoteData.Loading
    , count = 15
    }



-- { riders =
--     [ Rider "Tom Dumoulin" (RiderInfo 2 [ 1, 2, 3 ] "Team SunWeb")
--     , Rider "Lance Armstrong" (RiderInfo 1 [ 2, 3, 4 ] "US Postal Service")
--     ]
-- }


type alias RiderName =
    String


type alias Position =
    Int


type alias TeamName =
    String
