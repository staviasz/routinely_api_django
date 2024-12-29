from main.infra.repository.searchable import SearchParams, SearchResult


class TestSearchableParams:

    def test_searchable_params_prop_page(self):
        searchable_params = SearchParams()
        assert searchable_params.page == 1

        arrange = [
            {"page": 10, "expected": 10},
            {"page": -10, "expected": 1},
            {"page": "10", "expected": 10},
            {"page": 0, "expected": 1},
            {"page": "test", "expected": 1},
            {"page": "", "expected": 1},
            {"page": 5.5, "expected": 5},
            {"page": "5.5", "expected": 5},
            {"page": {}, "expected": 1},
            {"page": [], "expected": 1},
            {"page": True, "expected": 1},
            {"page": False, "expected": 1},
        ]

        for item in arrange:
            searchable_params = SearchParams({"page": item["page"]})
            print(item)
            assert searchable_params.page == item["expected"]

    def test_searchable_params_prop_per_page(self):
        searchable_params = SearchParams()
        assert searchable_params.per_page is None

        arrange = [
            {"per_page": 10, "expected": 10},
            {"per_page": -10, "expected": None},
            {"per_page": "10", "expected": 10},
            {"per_page": 0, "expected": None},
            {"per_page": "test", "expected": None},
            {"per_page": "", "expected": None},
            {"per_page": 5.5, "expected": 5},
            {"per_page": "5.5", "expected": 5},
            {"per_page": {}, "expected": None},
            {"per_page": [], "expected": None},
            {"per_page": False, "expected": None},
            {"per_page": True, "expected": None},
        ]

        for item in arrange:
            searchable_params = SearchParams({"per_page": item["per_page"]})

            assert searchable_params.per_page == item["expected"]

    def test_searchable_params_prop_sort(self):
        searchable_params = SearchParams()
        assert searchable_params.sort is None

        arrange = [
            {"sort": -10, "expected": None},
            {"sort": "10", "expected": "10"},
            {"sort": 0, "expected": None},
            {"sort": "test", "expected": "test"},
            {"sort": "", "expected": None},
            {"sort": " ", "expected": None},
            {"sort": "5.5", "expected": "5.5"},
            {"sort": {}, "expected": None},
            {"sort": [], "expected": None},
        ]

        for item in arrange:
            searchable_params = SearchParams({"sort": item["sort"]})
            assert searchable_params.sort == item["expected"]

    def test_searchable_params_prop_order(self):
        searchable_params = SearchParams()
        assert searchable_params.order is None

        arrange = [
            {"order": -10, "expected": None},
            {"order": "10", "expected": "asc"},
            {"order": 0, "expected": None},
            {"order": "test", "expected": "asc"},
            {"order": "", "expected": None},
            {"order": " ", "expected": "asc"},
            {"order": "5.5", "expected": "asc"},
            {"order": {}, "expected": None},
            {"order": [], "expected": None},
            {"order": "asc", "expected": "asc"},
            {"order": "ASC", "expected": "asc"},
            {"order": "desc", "expected": "desc"},
            {"order": "DESC", "expected": "desc"},
        ]

        for item in arrange:
            searchable_params = SearchParams({"order": item["order"]})
            print(item)
            print(searchable_params.order)
            assert searchable_params.order == item["expected"]


class TestSearchableResult:

    def test_searchable_result(self):
        data = {
            "items": [
                "entity1",
                "entity2",
                "entity3",
                "entity4",
                "entity5",
            ],
            "total": 15,
            "current_page": 1,
            "per_page": 6,
        }

        search = SearchResult(data)

        assert search.to_dict() == {**data, "last_page": 3, "order": None, "sort": None}

        data["order"] = "asc"
        data["sort"] = "name"
        search = SearchResult(data)

        assert search.to_dict() == {**data, "last_page": 3}
