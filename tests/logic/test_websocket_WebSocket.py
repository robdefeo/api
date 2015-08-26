from unittest import TestCase

from mock import Mock

from api.logic.websocket import WebSocket as Target


class fill_suggestions(TestCase):
    def test_regular(self):
        content = Mock()
        content.product_cache.side_effect = [
            {
                "_id": "new_suggestion_id_value_1"
            },
            {
                "_id": "new_suggestion_id_value_2"
            }
        ]
        target = Target(content, None)
        target.get_tile = Mock(
            side_effect=[
                "tile_1",
                "tile_2"
            ]
        )

        actual = target.fill_suggestions(
            [
                {
                    "_id": "_id_value_1",
                    "score": "suggestion_score_1",
                    "reasons": "suggestion_reasons_1",
                    "index": "suggestion_index_1"
                },
                {
                    "_id": "_id_value_2",
                    "score": "suggestion_score_2",
                    "reasons": "suggestion_reasons_2",
                    "index": "suggestion_index_2"
                }
            ]
        )
        self.assertListEqual(
            [{'_id': '_id_value_1', 'score': 'suggestion_score_1', 'tile': 'tile_1', 'position': 'suggestion_index_1',
              'reasons': 'suggestion_reasons_1'},
             {'_id': '_id_value_2', 'score': 'suggestion_score_2', 'tile': 'tile_2', 'position': 'suggestion_index_2',
              'reasons': 'suggestion_reasons_2'}],
            actual
        )

        self.assertEqual(2, target.get_tile.call_count)
        self.assertDictEqual(
            {
                'position': 'suggestion_index_1', '_id': '_id_value_1', 'reasons': 'suggestion_reasons_1',
                'score': 'suggestion_score_1', 'tile': 'tile_1'
            },
            target.get_tile.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {
                'position': 'suggestion_index_2', '_id': '_id_value_2', 'reasons': 'suggestion_reasons_2',
                'score': 'suggestion_score_2', 'tile': 'tile_2'
            },
            target.get_tile.call_args_list[1][0][0]
        )

        self.assertEqual(2, content.product_cache.call_count)
        self.assertEqual('_id_value_1', content.product_cache.call_args_list[0][0][0])
        self.assertEqual('_id_value_2', content.product_cache.call_args_list[1][0][0])


class on_next_page_message(TestCase):
    def test_regular(self):
        handler = Mock(name="handler_value")
        handler.context_id = "context_id_value"
        handler.user_id = "user_id_value"
        handler.application_id = "application_id_value"
        handler.session_id = "session_id_value"
        handler.locale = "locale_value"
        handler.suggest_id = "suggest_id_value"
        handler.page_size = "page_size_value"
        handler.offset = "original_offset_value"

        target = Target(None, None)

        target.get_suggestion_items = Mock(
            return_value=("suggestions_items_value", "new_offset_value")
        )

        target.write_suggestion_items = Mock()

        target.on_next_page_message(
            handler,
            {

            }
        )

        self.assertEqual(1, target.get_suggestion_items.call_count)
        self.assertEqual("user_id_value", target.get_suggestion_items.call_args_list[0][0][0])
        self.assertEqual("application_id_value", target.get_suggestion_items.call_args_list[0][0][1])
        self.assertEqual("session_id_value", target.get_suggestion_items.call_args_list[0][0][2])
        self.assertEqual("locale_value", target.get_suggestion_items.call_args_list[0][0][3])
        self.assertEqual("suggest_id_value", target.get_suggestion_items.call_args_list[0][0][4])
        self.assertEqual("page_size_value", target.get_suggestion_items.call_args_list[0][0][5])
        self.assertEqual("original_offset_value", target.get_suggestion_items.call_args_list[0][0][6])

        self.assertEqual("context_id_value", handler.context_id)
        self.assertEqual("suggest_id_value", handler.suggest_id)
        self.assertEqual("new_offset_value", handler.offset)

        self.assertEqual(1, target.write_suggestion_items.call_count)
        self.assertEqual(handler, target.write_suggestion_items.call_args_list[0][0][0])
        self.assertEqual("suggestions_items_value", target.write_suggestion_items.call_args_list[0][0][1])


class on_home_page_message(TestCase):
    def test_regular(self):
        handler = Mock(name="handler_value")
        handler.context_id = "context_id_value"
        handler.user_id = "user_id_value"
        handler.application_id = "application_id_value"
        handler.session_id = "session_id_value"
        handler.locale = "locale_value"
        handler.skip_mongodb_log = "skip_mongodb_log_value"
        handler.page_size = "page_size_value"
        handler.offset = "offset_value"

        target = Target(None, None)
        target.post_detect = Mock(
            return_value="detection_location_response"
        )
        target.get_detect = Mock(
            return_value="detection_response"
        )
        target.post_context_message_user = Mock(
            return_value="post_context_message_user_context_rev"
        )

        target.get_context = Mock(
            return_value="context_value"
        )

        target.post_suggest = Mock(
            return_value="suggest_id_value"
        )

        target.get_suggestion_items = Mock(
            return_value=("suggestions_items_value", "offset_value")
        )

        target.write_suggestion_items = Mock()

        target.on_home_page_message(
            handler,
            {
                "message_text": "message_text_value"
            }
        )

        self.assertEqual(1, target.post_detect.call_count)
        self.assertEqual("user_id_value", target.post_detect.call_args_list[0][0][0])
        self.assertEqual("application_id_value", target.post_detect.call_args_list[0][0][1])
        self.assertEqual("session_id_value", target.post_detect.call_args_list[0][0][2])
        self.assertEqual("locale_value", target.post_detect.call_args_list[0][0][3])
        self.assertEqual("message_text_value", target.post_detect.call_args_list[0][0][4])

        self.assertEqual(1, target.get_detect.call_count)

        self.assertEqual("detection_location_response", target.get_detect.call_args_list[0][0][0])

        self.assertEqual(1, target.post_context_message_user.call_count)
        self.assertEqual("context_id_value", target.post_context_message_user.call_args_list[0][0][0])
        self.assertEqual("detection_response", target.post_context_message_user.call_args_list[0][0][1])
        self.assertEqual("message_text_value", target.post_context_message_user.call_args_list[0][0][2])

        self.assertEqual(1, target.get_context.call_count)

        self.assertEqual(handler, target.get_context.call_args_list[0][0][0])

        self.assertEqual(1, target.post_suggest.call_count)
        self.assertEqual("user_id_value", target.post_suggest.call_args_list[0][0][0])
        self.assertEqual("application_id_value", target.post_suggest.call_args_list[0][0][1])
        self.assertEqual("session_id_value", target.post_suggest.call_args_list[0][0][2])
        self.assertEqual("locale_value", target.post_suggest.call_args_list[0][0][3])
        self.assertEqual("context_value", target.post_suggest.call_args_list[0][0][4])

        self.assertEqual(1, target.get_suggestion_items.call_count)
        self.assertEqual("user_id_value", target.get_suggestion_items.call_args_list[0][0][0])
        self.assertEqual("application_id_value", target.get_suggestion_items.call_args_list[0][0][1])
        self.assertEqual("session_id_value", target.get_suggestion_items.call_args_list[0][0][2])
        self.assertEqual("locale_value", target.get_suggestion_items.call_args_list[0][0][3])
        self.assertEqual("suggest_id_value", target.get_suggestion_items.call_args_list[0][0][4])
        self.assertEqual("page_size_value", target.get_suggestion_items.call_args_list[0][0][5])
        self.assertEqual(0, target.get_suggestion_items.call_args_list[0][0][6])

        self.assertEqual("context_id_value", handler.context_id)
        self.assertEqual("post_context_message_user_context_rev", handler.context_rev)
        self.assertEqual("suggest_id_value", handler.suggest_id)
        self.assertEqual("offset_value", handler.offset)

        self.assertEqual(1, target.write_suggestion_items.call_count)
        self.assertEqual(handler, target.write_suggestion_items.call_args_list[0][0][0])
        self.assertEqual("suggestions_items_value", target.write_suggestion_items.call_args_list[0][0][1])


class on_message(TestCase):
    def test_no_message_type(self):
        target = Target(None, None)
        target.on_home_page_message = Mock()

        self.assertRaises(
            Exception,
            target.on_message,
            {}
        )

        self.assertEqual(0, target.on_home_page_message.call_count)

    def test_unknown_message_type(self):
        target = Target(None, None)
        target.on_home_page_message = Mock()

        self.assertRaises(
            Exception,
            target.on_message,
            {
                "type": "unknown"
            }
        )

        self.assertEqual(0, target.on_home_page_message.call_count)

    def test_home_page_message(self):
        target = Target(None, None)
        target.on_home_page_message = Mock()
        target.on_next_page_message = Mock()

        target.on_message(
            "handler_value",
            {
                "type": "home_page_message"
            }
        )

        self.assertEqual(1, target.on_home_page_message.call_count)
        self.assertEqual("handler_value", target.on_home_page_message.call_args_list[0][0][0])
        self.assertDictEqual(
            {
                "type": "home_page_message"
            },
            target.on_home_page_message.call_args_list[0][0][1]
        )

        self.assertEqual(0, target.on_next_page_message.call_count)

    def test_next_page_message(self):
        target = Target(None, None)
        target.on_home_page_message = Mock()
        target.on_next_page_message = Mock()

        target.on_message(
            "handler_value",
            {
                "type": "next_page"
            }
        )

        self.assertEqual(0, target.on_home_page_message.call_count)
        self.assertEqual(1, target.on_next_page_message.call_count)
        self.assertEqual("handler_value", target.on_next_page_message.call_args_list[0][0][0])
        self.assertDictEqual(
            {
                "type": "next_page"
            },
            target.on_next_page_message.call_args_list[0][0][1]
        )


class on_close(TestCase):
    def test_found(self):
        client_handlers = {
            "existing_id": "existing_handler",
            "random_id": "other_handler"
        }
        target = Target(
            content=None,
            client_handlers=client_handlers
        )
        handler = Mock(name="new_client_handler")
        handler.id = "existing_id"
        target.on_close(handler)

        self.assertDictEqual(
            {'random_id': 'other_handler'},
            client_handlers
        )

    def test_not_found(self):
        client_handlers = {
            "random_id": "other_handler"
        }
        target = Target(
            content=None,
            client_handlers=client_handlers
        )
        handler = Mock(name="new_client_handler")
        handler.id = "existing_id"
        target.on_close(handler)

        self.assertDictEqual(
            {'random_id': 'other_handler'},
            client_handlers
        )


class open_Tests(TestCase):
    def test_context_id_not_None(self):
        target = Target(
            content=None,
            client_handlers={}
        )
        target.post_context = Mock()
        handler = Mock(name="new_client_handler")
        handler.id = "new_id"
        handler.context_id = "context_id_value"
        handler.context_rev = "context_rev_value"

        target.open(handler)

        self.assertEqual(0, target.post_context.call_count)

        self.assertEqual("context_rev_value", handler.context_rev)
        self.assertEqual("context_id_value", handler.context_id)

    def test_context_id_None(self):
        target = Target(
            content=None,
            client_handlers={}
        )
        target.get_context = Mock()
        target.post_context = Mock(
            return_value=("context_id_value", "context_rev_value")
        )
        handler = Mock()
        handler.context_id = None
        handler.user_id = "user_id_value"
        handler.application_id = "application_id_value"
        handler.session_id = "session_id_value"
        handler.locale = "locale_value"

        target.open(handler)

        self.assertEqual(0, target.get_context.call_count)
        self.assertEqual(1, target.post_context.call_count)

        self.assertEqual("user_id_value", target.post_context.call_args_list[0][0][0])
        self.assertEqual("application_id_value", target.post_context.call_args_list[0][0][1])
        self.assertEqual("session_id_value", target.post_context.call_args_list[0][0][2])
        self.assertEqual("locale_value", target.post_context.call_args_list[0][0][3])

        self.assertEqual(
            "context_id_value",
            handler.context_id
        )
        self.assertEqual(
            "context_rev_value",
            handler.context_rev
        )

    def test_new_id(self):
        client_handlers = {
            "different_id": "existing_handler"
        }
        target = Target(
            content=None,
            client_handlers=client_handlers
        )
        target.get_context = Mock(
            return_value="get_context_value"
        )
        target.post_context = Mock()
        handler = Mock(name="new_client_handler")
        handler.id = "new_id"
        handler.context_id = "context_id"
        handler._context = None

        target.open(handler)

        self.assertTrue("new_id" in client_handlers)
        self.assertEqual("new_id", client_handlers["new_id"].id)
        self.assertEqual("existing_handler", client_handlers["different_id"])

        self.assertEqual("context_id", handler.context_id)
        self.assertIsNone(handler._context)

        self.assertEqual(0, target.post_context.call_count)

    def test_existing_id(self):
        client_handlers = {
            "existing_id": "existing_handler"
        }

        target = Target(
            content=None,
            client_handlers=client_handlers
        )
        target.get_context = Mock(
            return_value="get_context_value"
        )
        target.post_context = Mock()
        handler = Mock(name="new_client_handler")
        handler.id = "existing_id"
        handler.context_id = "context_id"
        handler._context = None

        target.open(handler)

        self.assertTrue("existing_id" in client_handlers)
        self.assertEqual("existing_handler", client_handlers["existing_id"])
        self.assertEqual("context_id", handler.context_id)
        self.assertIsNone(handler._context)

        self.assertEqual(0, target.post_context.call_count)
