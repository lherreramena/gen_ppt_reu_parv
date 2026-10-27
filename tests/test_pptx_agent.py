import tempfile
import unittest
import zipfile
from pathlib import Path

from pptx_agent import ChangeError, apply_changes, extract_presentation


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def make_pptx(path):
    presentation = (
        f'<p:presentation xmlns:p="{P_NS}" xmlns:r="{R_NS}">'
        '<p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>'
    )
    relationships = (
        f'<Relationships xmlns="{REL_NS}"><Relationship Id="rId1" '
        'Type="slide" Target="slides/slide1.xml"/></Relationships>'
    )
    slide = (
        f'<p:sld xmlns:p="{P_NS}" xmlns:a="{A_NS}"><p:cSld><p:spTree>'
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/></p:nvSpPr><p:txBody>'
        '<a:p><a:r><a:t>Original title</a:t></a:r></a:p></p:txBody></p:sp>'
        '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Subtitle"/></p:nvSpPr><p:txBody>'
        '<a:p><a:r><a:t>Keep this text</a:t></a:r></a:p></p:txBody></p:sp>'
        '</p:spTree></p:cSld></p:sld>'
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ppt/presentation.xml", presentation)
        archive.writestr("ppt/_rels/presentation.xml.rels", relationships)
        archive.writestr("ppt/slides/slide1.xml", slide)
        archive.writestr("ppt/media/image1.png", b"unchanged media")


class PptxAgentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.template = Path(self.temp_dir.name) / "template.pptx"
        self.output = Path(self.temp_dir.name) / "result.pptx"
        make_pptx(self.template)

    def test_extracts_text_by_slide_and_shape_id(self):
        self.assertEqual(
            extract_presentation(self.template),
            [
                {
                    "slide": 1,
                    "shapes": [
                        {"shape_id": 2, "text": "Original title"},
                        {"shape_id": 3, "text": "Keep this text"},
                    ],
                }
            ],
        )

    def test_changes_only_requested_shape_and_preserves_other_package_parts(self):
        with zipfile.ZipFile(self.template) as original:
            untouched_media = original.read("ppt/media/image1.png")
            untouched_shape = original.read("ppt/slides/slide1.xml")
        plan = {
            "changes": [
                {
                    "slide": 1,
                    "shape_id": 2,
                    "original_text": "Original title",
                    "new_text": "Updated title",
                }
            ]
        }

        apply_changes(self.template, self.output, plan)

        with zipfile.ZipFile(self.output) as result:
            self.assertEqual(result.read("ppt/media/image1.png"), untouched_media)
            self.assertNotEqual(result.read("ppt/slides/slide1.xml"), untouched_shape)
        self.assertEqual(
            extract_presentation(self.output)[0]["shapes"],
            [
                {"shape_id": 2, "text": "Updated title"},
                {"shape_id": 3, "text": "Keep this text"},
            ],
        )

    def test_rejects_stale_original_text_without_creating_output(self):
        plan = {
            "changes": [
                {
                    "slide": 1,
                    "shape_id": 2,
                    "original_text": "Unexpected title",
                    "new_text": "Updated title",
                }
            ]
        }
        with self.assertRaises(ChangeError):
            apply_changes(self.template, self.output, plan)
        self.assertFalse(self.output.exists())

    def test_rejects_paragraph_count_changes(self):
        plan = {
            "changes": [
                {
                    "slide": 1,
                    "shape_id": 2,
                    "original_text": "Original title",
                    "new_text": "First\nSecond",
                }
            ]
        }
        with self.assertRaises(ChangeError):
            apply_changes(self.template, self.output, plan)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
