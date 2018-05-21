module View exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, type_)
import Models exposing (..)
import Msgs exposing (Msg)
import RemoteData exposing (WebData)
import LineChart
import LineChart.Colors as Colors
import LineChart.Dots as Dots


view : Model -> Html Msg
view response =
    div []
        [ div [ class "right-box" ]
            [ nav
            , maybeList response.riders response.count
            ]
        , div
            [ class "left-box" ]
            [ maybeChart response.riders response.count
            ]
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


maybeChart : WebData (List Rider) -> Int -> Html Msg
maybeChart response count =
    case response of
        RemoteData.NotAsked ->
            text ""

        RemoteData.Loading ->
            text "loading"

        RemoteData.Success riders ->
            chart (List.take count riders)

        RemoteData.Failure error ->
            text (toString error)


chart : List Rider -> Html Msg
chart riders =
    LineChart.view .stage
        .time
        (List.map lineRider riders)


lineRider : Rider -> LineChart.Series StageTime
lineRider rider =
    LineChart.line Colors.purple Dots.cross rider.name (plotifyTimes rider.info.times)


plotifyTimes : List Int -> List StageTime
plotifyTimes times =
    times
        |> List.indexedMap (\idx gap -> { stage = (toFloat idx + 1), time = (toFloat gap) })


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
            , text ("#" ++ (toString rider.info.position) ++ " " ++ rider.name)
            ]
        ]
