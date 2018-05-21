module View exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, type_)
import Models exposing (..)
import Msgs exposing (Msg)
import RemoteData exposing (WebData)


view : Model -> Html Msg
view response =
    div [ class "right-box" ]
        [ nav
        , maybeList response.riders response.count
        ]


maybeList : WebData (List Rider) -> Int -> Html Msg
maybeList response count =
    case response of
        RemoteData.NotAsked ->
            text ""

        RemoteData.Loading ->
            text "loading"

        RemoteData.Success riders ->
            list riders count

        RemoteData.Failure error ->
            text (toString error)


nav : Html Msg
nav =
    div [ class "cleafix mb2" ]
        [ div [ class "left p2" ]
            [ text "Select riders" ]
        ]


list : List Rider -> Int -> Html Msg
list riders count =
    div [ class "p1" ]
        (List.take count riders |> List.map riderCheck)


riderCheck : Rider -> Html Msg
riderCheck rider =
    div []
        [ br [] []
        , label []
            [ input [ type_ "checkbox" ] []
            , text rider.name
            ]
        ]
