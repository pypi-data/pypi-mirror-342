"""A class for handling windowed plackett luce ratings."""

# pylint: disable=too-many-locals,too-many-branches,too-many-statements,too-few-public-methods,too-many-nested-blocks

import datetime

import pandas as pd
from openskill.models import PlackettLuce, PlackettLuceRating

from .identifier import Identifier
from .match import Match
from .team import Team


class WindowedRating:
    """Handles plackett luce ratings based on windows."""

    _team_ratings: dict[str, PlackettLuceRating]
    _player_ratings: dict[str, PlackettLuceRating]
    _matches: list[Match]

    def __init__(self, window: datetime.timedelta | None, dt_column: str):
        self.window = window
        self._dt_column = dt_column
        self._team_model = PlackettLuce()
        self._player_model = PlackettLuce()
        self._team_ratings = {}
        self._player_ratings = {}
        self._matches = []

    def add(
        self,
        row: pd.Series,
        team_identifiers: list[Identifier],
        player_identifiers: list[Identifier],
    ) -> tuple[
        dict[str, tuple[PlackettLuceRating, int, float]],
        dict[str, tuple[PlackettLuceRating, int, float]],
    ]:
        """Add a new row to the windowed rating."""
        teams = []
        for team_identifier in team_identifiers:
            if team_identifier.column not in row:
                continue
            team_id = row[team_identifier.column]
            if pd.isnull(team_id):
                continue
            if team_id not in self._team_ratings:
                self._team_ratings[team_id] = self._team_model.rating(name=team_id)

            team_player_ids = []
            for player_identifier in player_identifiers:
                if player_identifier.team_identifier_column is None:
                    continue
                if player_identifier.team_identifier_column not in row:
                    continue
                player_team_id = row[player_identifier.team_identifier_column]
                if pd.isnull(player_team_id):
                    continue
                if player_team_id != team_id:
                    continue
                if player_identifier.column not in row:
                    continue
                player_id = row[player_identifier.column]
                if pd.isnull(player_id):
                    continue
                team_player_ids.append(player_id)
                if player_id not in self._player_ratings:
                    self._player_ratings[player_id] = self._player_model.rating(
                        name=player_id
                    )

            points = None
            if (
                team_identifier.points_column is not None
                and team_identifier.points_column in row
            ):
                points = row[team_identifier.points_column]
            teams.append(Team(team_player_ids, points, team_id))

        match = Match(teams, row[self._dt_column].to_pydatetime())

        if self.window is not None:
            # Remove older matches and reverse their results.
            oldest_dt = match.dt - self.window
            remove_matches = [x for x in self._matches if x.dt < oldest_dt]
            for remove_match in remove_matches:
                scores: list[float] | None = [
                    x.points
                    for x in reversed(remove_match.teams)
                    if x.points is not None
                ]
                if not scores:
                    scores = None
                if len(remove_match.teams) >= 2:
                    team_ratings: list[list[PlackettLuceRating]] = [
                        [self._team_ratings[x.identifier]] for x in remove_match.teams
                    ]
                    team_ratings = self._team_model.rate(
                        team_ratings,
                        scores=scores,
                    )
                    for team_rating in team_ratings:
                        self._team_ratings[str(team_rating[0].name)] = team_rating[0]
                    if all(x.players for x in remove_match.teams):
                        players = self._player_model.rate(
                            [
                                [self._player_ratings[y] for y in x.players]
                                for x in remove_match.teams
                            ],
                            scores=scores,
                        )
                        for player_rating in players:
                            for player_subrating in player_rating:
                                self._player_ratings[str(player_subrating.name)] = (
                                    player_subrating
                                )
            self._matches = self._matches[len(remove_matches) :]

        # Find the results
        team_result = {}
        player_result = {}
        if len(match.teams) >= 2:
            team_rank = self._team_model.predict_rank(
                [[self._team_ratings[x.identifier]] for x in match.teams]
            )
            team_result = {
                x.identifier: (
                    self._team_ratings[x.identifier],
                    team_rank[count][0],
                    team_rank[count][1],
                )
                for count, x in enumerate(match.teams)
            }
            if all(x.players for x in match.teams):
                player_rank = self._player_model.predict_rank(
                    [[self._player_ratings[y] for y in x.players] for x in match.teams]
                )
                for count, team in enumerate(match.teams):
                    for player in team.players:
                        player_result[player] = (
                            self._player_ratings[player],
                            player_rank[count][0],
                            player_rank[count][1],
                        )

        # Record the new match results
        scores = [x.points for x in match.teams if x.points is not None]
        if not scores:
            scores = None
        if len(match.teams) >= 2:
            team_ratings = self._team_model.rate(
                [[self._team_ratings[x.identifier]] for x in match.teams], scores=scores
            )
            for team_rating in team_ratings:
                self._team_ratings[str(team_rating[0])] = team_rating[0]
            if all(x.players for x in match.teams):
                player_ratings: list[list[PlackettLuceRating]] = (
                    self._player_model.rate(
                        [
                            [self._player_ratings[y] for y in x.players]
                            for x in match.teams
                        ],
                        scores=scores,
                    )
                )
                for player_rating in player_ratings:
                    for player_subrating in player_rating:
                        self._player_ratings[str(player_subrating.name)] = (
                            player_subrating
                        )
        self._matches.append(match)

        return team_result, player_result
