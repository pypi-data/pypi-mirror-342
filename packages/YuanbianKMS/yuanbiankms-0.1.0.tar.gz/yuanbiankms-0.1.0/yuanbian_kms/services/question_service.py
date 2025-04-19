# -*- coding=utf-8 -*-
import datetime
import time
from datetime import timedelta
from xp_cms.services.base_service import DocumentBaseService, XPService
from xp_cms.models.question import QuestionDocument, QuestionOptionDocument, \
    ExerciseLogDocument, ExerciseQuestionDocument, TestingDocument, InternshipScore


class InternshipScoreLogService(XPService):
    model = InternshipScore


class QuestionDocumentService(DocumentBaseService):
    model = QuestionDocument
    option_model = QuestionOptionDocument

    @classmethod
    def add(cls, question_data, option_data):
        question_document = cls.model(**question_data)
        question_document.q_option = [cls.option_model(
            **option
        ) for option in option_data]
        try:
            question_document.save()
        except Exception as e:
            raise e
        else:
            return question_document

    @classmethod
    def delete_by_id(cls, document_id):
        return cls.model.objects(id=document_id).delete()

    @classmethod
    def update(cls, document, data, options):
        # data['pk'] = pk
        document.q_correct_option = 0
        document.q_correct_options = []
        document.q_option = [cls.option_model(**option) for option in options]
        return document.save()


class ExerciseLogDocumentService(DocumentBaseService):
    model = ExerciseLogDocument
    question_model = ExerciseQuestionDocument

    @classmethod
    def add_new_log(cls, username, testing_doc):
        question_ids = []
        for q_type_id, q in testing_doc.question_combination.items():
            question_ids.extend([str(idx['_id']) for idx in
                                 QuestionDocumentService.get_sample({"q_type_id": q_type_id}, int(q['num']))])
        exercise_log_document = {"username"     : username,
                                 "testing_id"   : testing_doc.pk,
                                 "testing_title": testing_doc.title,
                                 "score"        : 0,
                                 "answer_log"   : {},
                                 "question_ids" : question_ids,
                                 "start_time"   : round(time.time()),
                                 "is_internship": testing_doc.is_internship,
                                 "college_name": testing_doc.college_name
                                 }
        return ExerciseLogDocumentService.add(exercise_log_document)

    @classmethod
    def add_question(cls, data):
        return cls.question_model(**data)

    @classmethod
    def get_ownerlog_by_id(cls, log_id, username):
        return cls.model.objects(id=log_id, username=username).first()

    @classmethod
    def get_wait_finish_log(cls, username, testing_id):
        return cls.model.objects(username=username, testing_id=testing_id, finish=False).first()

    @classmethod
    def count(cls, username):
        return cls.model.objects(username=username).count()

    @classmethod
    def count_success(cls, username):
        return cls.model.objects(username=username, success=True).count()

    @classmethod
    def avg_score(cls, username):
        return cls.model.objects(username=username).average('score')

    @classmethod
    def group_by_testing_id(cls, username):
        pipeline = [{"$match":{"username":username}},
                    {"$group": {"_id":'$testing_id', "count": {"$sum": 1}, "title":{"$first": "$testing_title"}}},
                    ]
        # objects = cls.model.objects(username=username)
        return cls.model.objects.aggregate(pipeline)

    @classmethod
    def last_week(cls, username):
        return cls.model.objects(username=username,
                                 finish_time__gte=(datetime.datetime.now()-timedelta(weeks=1)).timestamp()).all()



class TestingDocumentService(DocumentBaseService):
    model = TestingDocument