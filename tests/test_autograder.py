def test_submission_path_fixture(pytester):
    pytester.makepyfile("""
        from pathlib import Path

        def test_submission_path(submission_path):
            assert submission_path == Path(".")
    """)

    result = pytester.runpytest(
        '--submission-path=.',
        '-v'
    )

    result.stdout.fnmatch_lines([
        '*::test_submission_path PASSED*',
    ])

    assert result.ret == 0
