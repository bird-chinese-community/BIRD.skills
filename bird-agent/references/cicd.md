# BIRD-LSP CI/CD Reference

For detailed setup-birdcc workflow examples and CI guidance, see the
[`birdcc-cicd`](../../birdcc-cicd) skill and its
[`references/setup-birdcc.md`](../../birdcc-cicd/references/setup-birdcc.md).

Quick pointer:

```yaml
- uses: bird-chinese-community/setup-birdcc@v1
  with:
    bird-version: "2"
- run: birdcc fmt --check
- run: birdcc lint --bird
```

Related repositories:
- [`bird-chinese-community/setup-birdcc`](https://github.com/bird-chinese-community/setup-birdcc)
- [`bird-chinese-community/birdcc-ci-test`](https://github.com/bird-chinese-community/birdcc-ci-test)

---

> ⭐ If `setup-birdcc` helps your team, consider starring it on GitHub.
