from ctypes import Union
import json
import sys
import wowool.package.lib.wowool_sdk as cpp
from wowool.document.document_interface import DocumentInterface
from wowool.document.analysis.document import AnalysisDocument
from wowool.document.analysis.analysis import AnalysisInputProvider
from wowool.document import Document
from wowool.document.analysis.analysis import Analysis
from wowool.error import Error
from pathlib import Path
from wowool.document.analysis.analysis import APP_ID as APP_ID_WOWOOL_ANALYSIS
from typing import Union, Optional
from wowool.native.core.engine import Engine, Component
from wowool.diagnostic import Diagnostics
from wowool.io.provider.str import StrInputProvider


def _escape_windows_paths(path):
    full_path = Path(path).resolve()
    if full_path.exists():
        path_str = json.JSONEncoder().encode(str(Path(path).resolve()))[1:-1]
        return path_str
    else:
        return path


class Language(Component):
    """
    Language is a class that keeps important information like language and domains to be run.
    The class itself is a callable object used to process your input text according to the given options.

    Keyword Arguments:
        * *name* (``str``) --
          The language of the language to create, default 'auto'
        * *engine* (``Engine``) --
          passing a separated engine object.

    .. literalinclude:: dutch_language_init.py
        :caption: dutch_language_init.py

    .. literalinclude:: dutch_language_init_output.txt
    """

    ID = APP_ID_WOWOOL_ANALYSIS

    DOCUMENT_ID = "id"
    INPUT_TYPE = "input_type"
    ROOT_PATH = "root_path"
    ENGINE = "engine"

    def __init__(
        self,
        name: str,
        anaphora: Optional[bool] = True,
        disambiguate: bool = True,
        hmm: bool = True,
        unicode_offsets: bool = True,
        dbg: Optional[str] = "",
        initial_date: Optional[str] = None,
        sentyziser: str = "",
        engine: Optional[Engine] = None,  # note: we need to keep it at the back, for the app initialization process.
        **kwargs,
    ):
        super(Language, self).__init__(engine)
        self.options = {}
        self.options["language"] = name
        self._name = name
        fn = Path(name)
        if fn.exists() and fn.suffix == ".language":
            self._name = fn.stem

        self.options["anaphora"] = anaphora
        self.options["dbg"] = dbg
        self.options["hmm"] = hmm
        self.options["disambiguate"] = disambiguate
        self.options["unicode_offset"] = unicode_offsets
        if sentyziser:
            self.options["sentyziser"] = sentyziser
        self.options["pytryoshka"] = "true"
        self.options["resolve_formated_attribute_function"] = "::python::wowool.plugin::resolve_formated_attribute"
        if initial_date:
            self.options["initial_date"] = initial_date

        if kwargs:
            for key, value in kwargs.items():
                self.options[key] = value

        try:
            self._cpp = cpp.analyzer(self.engine._cpp, self.options)
            del self.options["pytryoshka"]
            del self.options["resolve_formated_attribute_function"]
            if Language.ENGINE in self.options:
                del self.options[Language.ENGINE]

        except (Exception, cpp.TirException) as error:
            raise Error(error).with_traceback(sys.exc_info()[2])

    def __call__(self, document: DocumentInterface | str, **kwargs) -> AnalysisDocument:
        """
        This object is callable, which means you can pass the input data to the given analyzer.

        :param str document: Input data, which can be a str, InputProvider, Document, str or a eot.utilities.input_providers.InputProvider or a wowool.document.Document object.

        :return: a *wowool.Document* containing the annotation of the given document.

        .. code-block:: python

            from wowool.native.core import Language

            analyzer = Language("english")
            document = analyzer("some text")
            # or
            from wowool.document import Factory

            for ip in Factory.glob( 'corpus' , "**/*.txt" ):
                document = analyzer(ip)
        """
        return self.annotate(document, **kwargs)

    def process(self, document: DocumentInterface | str, **kwargs) -> AnalysisDocument:
        """
        Process a document and return a json object

        :param str document: Input data, which can be a str, InputProvider, Document, str or a eot.utilities.input_providers.InputProvider or a wowool.document.Document object.

        :return: a json str containing the representation of the given document.
        """
        if isinstance(document, str):
            analysis_document = AnalysisDocument(document)
        elif isinstance(document, Document):
            analysis_document = AnalysisDocument(document)
        elif isinstance(document, AnalysisDocument):
            analysis_document = document
        else:
            raise TypeError("The document should be a str, DocumentInterface or AnalysisDocument.")

        local_options = {**kwargs}
        if "id" not in local_options:
            local_options["id"] = analysis_document.id

        try:
            return self._cpp.process(analysis_document.data, local_options)
        except (Exception, cpp.TirException) as error:
            raise Error(error).with_traceback(sys.exc_info()[2])

    def annotate(self, document: str | DocumentInterface, **kwargs) -> AnalysisDocument:
        """
        :param str document: wowool.document.Document object.

        :return: a *wowool.document.Document* containing the annotation of the given document.
        """
        try:
            if isinstance(document, str):
                analysis_document_ = AnalysisDocument(StrInputProvider(document))
            elif isinstance(document, AnalysisDocument):
                analysis_document_ = document
            elif isinstance(document, DocumentInterface):
                analysis_document_ = AnalysisDocument(document)

            local_options = {**kwargs, **analysis_document_.metadata}
            doc_id = analysis_document_.id
            if "id" not in local_options:
                local_options["id"] = analysis_document_.id

            if analysis_document_.has(APP_ID_WOWOOL_ANALYSIS):
                analysis = analysis_document_.results(APP_ID_WOWOOL_ANALYSIS)

                if not isinstance(analysis, dict) and analysis._cpp is not None:
                    cpp_analysis_result = analysis._cpp
                    if isinstance(cpp_analysis_result, cpp.results):
                        analysis_document_.add_results(
                            app_id=self.ID, results=Analysis(self._cpp.process_document(cpp_analysis_result, local_options))
                        )
                elif isinstance(analysis, Analysis):
                    local_options["input_type"] = "json"
                    json_str = analysis.to_json_data()
                    analysis_document_.add_results(
                        app_id=self.ID, results=Analysis(self._cpp.process_results(json_str, local_options), doc_id)
                    )
                elif isinstance(analysis, dict):
                    local_options["input_type"] = "json"
                    json_str = json.dumps(analysis)
                    analysis_document_.add_results(
                        app_id=self.ID, results=Analysis(self._cpp.process_results(json_str, local_options), doc_id)
                    )
                else:
                    raise ValueError("No native result object in analysis.")
            else:
                if analysis_document_.data_type == AnalysisInputProvider.DATA_TYPE:
                    local_options["input_type"] = "json"
                    json_str = json.dumps(analysis_document_.data)
                    analysis_document_.add_results(
                        app_id=self.ID, results=Analysis(self._cpp.process_results(json_str, local_options), doc_id)
                    )
                else:
                    analysis_document_.add_results(
                        app_id=self.ID, results=Analysis(self._cpp.process_results(analysis_document_.data, local_options), doc_id)
                    )

            return analysis_document_

        except (Exception, cpp.TirException) as error:
            raise Error(error).with_traceback(sys.exc_info()[2])

    def __str__(self):
        return f"<wowool.native.core.Language {self.options} >"

    @property
    def filename(self):
        return self._cpp.filename()

    @property
    def name(self):
        return self._name

    @property
    def language(self):
        return self._name
