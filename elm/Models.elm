module Models exposing (..)

import RemoteData exposing (WebData)
import List.Extra exposing (zip)


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


gapToRider : Rider -> Rider -> List Int
gapToRider reference rider =
    rider.info.times
        |> zip reference.info.times
        |> List.map (\( ref, rid ) -> rid - ref)


type alias RiderName =
    String


type alias StageTime =
    { stage : Float
    , time : Float
    }


type alias Position =
    Int


type alias TeamName =
    String
