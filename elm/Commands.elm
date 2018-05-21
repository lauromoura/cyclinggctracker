module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)
import Msgs exposing (Msg)
import Models exposing (Rider, RiderInfo)
import RemoteData


fetchRiders : Cmd Msg
fetchRiders =
    Http.get fetchRidersUrl ridersDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchRiders


fetchRidersUrl : String
fetchRidersUrl =
    "./data/output.json"


ridersDecoder : Decode.Decoder (List Rider)
ridersDecoder =
    Decode.list riderDecoder


riderDecoder : Decode.Decoder Rider
riderDecoder =
    decode Rider
        |> required "name" Decode.string
        |> required "info" riderInfoDecoder


riderInfoDecoder : Decode.Decoder RiderInfo
riderInfoDecoder =
    decode RiderInfo
        |> required "position" Decode.int
        |> required "times" (Decode.list Decode.int)
        |> required "team" Decode.string
