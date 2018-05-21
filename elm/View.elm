module View exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, type_)
import Models exposing (..)
import Msgs exposing (Msg)


view : Model -> Html Msg
view model =
    div []
        [ nav
        , list model.riders
        ]


nav : Html Msg
nav =
    div [ class "cleafix mb2" ]
        [ div [ class "left p2" ]
            [ text "Select riders" ]
        ]


list : List Rider -> Html Msg
list riders =
    div [ class "p1" ]
        (List.map riderCheck riders)


riderCheck : Rider -> Html Msg
riderCheck rider =
    div []
        [ br [] []
        , label []
            [ input [ type_ "checkbox" ] []
            , text rider.name
            ]
        ]
