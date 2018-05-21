module Main exposing (..)

import Html exposing (program)
import Models exposing (Model, initialModel)
import Msgs exposing (Msg)
import View exposing (view)
import Update exposing (update)


init : ( Model, Cmd Msg )
init =
    ( initialModel, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
