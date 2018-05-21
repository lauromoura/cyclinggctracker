module Models exposing (..)


type alias Model =
    { riders : List Rider
    }


type alias Rider =
    { name : String
    , position : Position
    , times : List Int
    , team : String
    }


initialModel : Model
initialModel =
    { riders =
        [ Rider "Tom Dumoulin" 2 [ 1, 2, 3 ] "Team SunWeb"
        , Rider "Lance Armstrong" 1 [ 2, 3, 4 ] "US Postal Service"
        ]
    }


type alias RiderName =
    String


type alias Position =
    Int


type alias TeamName =
    String
