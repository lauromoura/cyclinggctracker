module Msgs exposing (..)

import Models exposing (Rider)
import RemoteData exposing (WebData)


type Msg
    = OnFetchRiders (WebData (List Rider))
